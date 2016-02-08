#!/usr/bin/env python

# SOMATYPUS: A PLATYPUS-BASED VARIANT CALLING PIPELINE FOR CANCER DATA
# Adrian Baez-Ortega, Transmissible Cancer Group, University of Cambridge
# 22/01/2016

# Somatypus_SnpMerge.py
# Merges SNPs from multiple Platypus output VCF files
# Called by merge_calls()

# INPUT
# inputFile: text file with paths to VCF files, one per line
# excludeFile: text file with a list of SNPs to exclude, in CHROM:POS,REF>ALT format
# outDir: path to (existing) output folder

 
"""
This script is used to merge SNPs from multiple Platypus VCFs. In each VCF, it selects only SNPs 
that are not included in the list of SNPs to exclude (SNPs near indels, in principle). 
For multiallelic SNPs, it outputs extra alleles to different files for independent genotyping.
"""


import sys
import gzip
import os
import re
from sets import Set


# If not 3 arguments: print help
if len(sys.argv) != 4:
    print '\nSomatypus_SnpMerge.py: Merges SNPs from multiple Platypus output VCF files.'
    print '                       *The VCFs need to be split first using the Somatypus_SplitMAandMNPs.py script.*'
    print '                       *The exclusion list has to be created using the Somatypus_IndelFlag.py script.*'
    print '                       For each VCF, it selects only SNPs that are not included in the list of SNPs'
    print '                       to exclude (SNPs located at <5 bp from an indel, in principle).'
    print '                       For multiallelic SNPs, it outputs extra alleles to different files for'
    print '                       independent genotyping.\n'
    print '                Input: A text file with paths to VCF files, one per line.'
    print '                       A text file with a list of SNPs to exclude, in CHROM:POS,REF>ALT format.'
    print '                       Path to (existing) output folder.'
    print '                Usage: Somatypus_SnpMerge.py /path/to/fileList.txt /path/to/excludeList.txt /path/to/outDir\n'
    sys.exit(0)


script, inputFile, excludeFile, outDir = sys.argv


# Read list of SNPs to exclude (<5bp from an indel in any sample)
print '\nReading list of SNPs to exclude from file ' + excludeFile
flaggedSNPs = Set([])
with open(excludeFile, 'r') as excludeList:
    flaggedSNPs = Set(line.strip() for line in excludeList)
    

# Extract SNPs from each sample, if they are not in the exclude list
mergedSNPs = {}
excludedSNPs = {}
with open(inputFile, 'r') as vcfList:
    for listLine in vcfList:
        vcfFile = listLine.strip()
        print 'Extracting SNPs from file ' + vcfFile
        with open(vcfFile, 'r') as vcf:
            for line in vcf:
                if not line.startswith('#'):
                    col = line.strip().split('\t')
                    chrom = col[0]
                    pos = col[1]
                    ref = col[3]
                    alt = col[4]
                    # Check for MA variants
                    if ',' in alt:
                        print '\nERROR: Multiallelic variant found at ' + chrom + ':' + pos + '. Use splitMAandMNPs.py first.\n'
                        sys.exit(1)

                    # For each SNP: if in flagged list, write to excluded SNPs set; else, write to merged SNPs set
                    if len(ref) == len(alt):
                        # Check for MNPs
                        if len(ref) != 1:
                            print '\nERROR: MNP found at ' + chrom + ':' + pos + '. Use splitMAandMNPs.py first.\n'
                            sys.exit(1)
                        id = chrom + ':' + pos + ',' + ref + '>' + alt
                        if id in flaggedSNPs and id not in excludedSNPs:
                            excludedSNPs[id] = line
                        if id not in flaggedSNPs and id not in mergedSNPs:
                            mergedSNPs[id] = line


# Compose paths of output VCF files
outFile1 = outDir + '/MergedSNPs_allele1.vcf'
outFile2 = outDir + '/MergedSNPs_allele2.vcf'
outFile3 = outDir + '/MergedSNPs_allele3.vcf'
outFileF1 = outDir + '/IndelExcludedSNPs_allele1.vcf'
outFileF2 = outDir + '/IndelExcludedSNPs_allele2.vcf'
outFileF3 = outDir + '/IndelExcludedSNPs_allele3.vcf'
print '\nMerging non-excluded SNPs into files ' + outFile1
print '                                     ' + outFile2
print '                                     ' + outFile3
print '\nMerging indel-excluded SNPs into files ' + outFileF1
print '                                       ' + outFileF2
print '                                       ' + outFileF3


# Write merged, de-duplicated SNPs to output file corresponding to its allele number
with open(outFile1, 'w') as out1, open(outFile2, 'w') as out2, open(outFile3, 'w') as out3:
    lastPos = ''
    second = False
    for id in sorted(mergedSNPs):
        pos = id.split(',')[0]
        if lastPos != pos:
            out1.write(mergedSNPs[id])
            lastPos = pos
            second = False
        elif not second:
            out2.write(mergedSNPs[id])
            second = True
        else:
            out3.write(mergedSNPs[id])
            second = False


# Write merged indel-excluded SNPs to output file corresponding to its allele number
with open(outFileF1, 'w') as out1, open(outFileF2, 'w') as out2, open(outFileF3, 'w') as out3:
    lastPos = ''
    second = False
    for id in sorted(excludedSNPs):
        pos = id.split(',')[0]
        if lastPos != pos:
            out1.write(excludedSNPs[id])
            lastPos = pos
            second = False
        elif not second:
            out2.write(excludedSNPs[id])
            second = True
        else:
            out3.write(excludedSNPs[id])
            second = False

print '\nDone!\n'
