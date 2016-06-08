#!/usr/bin/env python

# SOMATYPUS: A PLATYPUS-BASED VARIANT CALLING PIPELINE FOR CANCER DATA
# Adrian Baez-Ortega, Transmissible Cancer Group, University of Cambridge
# 22/01/2016

# Somatypus_SnpMerge.py
# Merges SNVs from multiple Platypus output VCF files
# Called by merge_calls()

# INPUT
# inputFile: text file with paths to VCF files, one per line
# excludeFile: text file with a list of SNVs to exclude, in CHROM:POS,REF>ALT format
# outDir: path to (existing) output folder

 
"""
This script is used to merge SNVs from multiple Platypus VCFs. In each VCF, it selects only SNVs 
that are not included in the list of SNVs to exclude (SNVs near indels, in principle). 
For multiallelic SNVs, it outputs extra alleles to different files for independent genotyping.
"""


import sys
import os
import re
from sets import Set


# If not 3 arguments: print help
if len(sys.argv) != 4:
    print '\nSomatypus_SNVmerge.py: Merges SNVs from multiple Platypus output VCF files.'
    print '                       *The VCFs need to be split first using the Somatypus_SplitMAandMNPs.py script.*'
    print '                       *The exclusion list has to be created using the Somatypus_IndelFlag.py script.*'
    print '                       For each VCF, it selects only SNVs that are not included in the list of SNVs'
    print '                       to exclude (SNVs located at <5 bp from an indel, in principle).'
    print '                       For multiallelic SNVs, it outputs extra alleles to different files for'
    print '                       independent genotyping.\n'
    print '                Input: A text file with paths to VCF files, one per line.'
    print '                       A text file with a list of SNVs to exclude, in CHROM:POS,REF>ALT format.'
    print '                       Path to (existing) output folder.'
    print '                Usage: Somatypus_SNVmerge.py /path/to/fileList.txt /path/to/excludeList.txt /path/to/outDir\n'
    sys.exit(0)


script, inputFile, excludeFile, outDir = sys.argv


# Read list of SNVs to exclude (<5bp from an indel in any sample)
print '\nReading list of SNVs to exclude from file ' + excludeFile
flaggedSNVs = Set([])
with open(excludeFile, 'r') as excludeList:
    flaggedSNVs = Set(line.strip() for line in excludeList)
    

# Extract SNVs from each sample, if they are not in the exclude list
mergedSNVs = {}
excludedSNVs = {}
with open(inputFile, 'r') as vcfList:
    for listLine in vcfList:
        vcfFile = listLine.strip()
        print 'Extracting SNVs from file ' + vcfFile
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

                    # For each SNV: if in flagged list, write to excluded SNVs set; else, write to merged SNVs set
                    if len(ref) == len(alt):
                        # Check for MNPs
                        if len(ref) != 1:
                            print '\nERROR: MNP found at ' + chrom + ':' + pos + '. Use splitMAandMNPs.py first.\n'
                            sys.exit(1)
                        id = chrom + ':' + pos + ',' + ref + '>' + alt
                        if id in flaggedSNVs and id not in excludedSNVs:
                            excludedSNVs[id] = line
                        if id not in flaggedSNVs and id not in mergedSNVs:
                            mergedSNVs[id] = line


# Compose paths of output VCF files
outFile1 = outDir + '/MergedSNVs_allele1.vcf'
outFile2 = outDir + '/MergedSNVs_allele2.vcf'
outFile3 = outDir + '/MergedSNVs_allele3.vcf'
outFileF1 = outDir + '/IndelExcludedSNVs_allele1.vcf'
outFileF2 = outDir + '/IndelExcludedSNVs_allele2.vcf'
outFileF3 = outDir + '/IndelExcludedSNVs_allele3.vcf'
print '\nMerging non-excluded SNVs into files ' + outFile1
print '                                     ' + outFile2
print '                                     ' + outFile3
print '\nMerging indel-excluded SNVs into files ' + outFileF1
print '                                       ' + outFileF2
print '                                       ' + outFileF3


# Write merged, de-duplicated SNVs to output file corresponding to its allele number
with open(outFile1, 'w') as out1, open(outFile2, 'w') as out2, open(outFile3, 'w') as out3:
    lastPos = ''
    second = False
    for id in sorted(mergedSNVs):
        pos = id.split(',')[0]
        if lastPos != pos:
            out1.write(mergedSNVs[id])
            lastPos = pos
            second = False
        elif not second:
            out2.write(mergedSNVs[id])
            second = True
        else:
            out3.write(mergedSNVs[id])
            second = False


# Write merged indel-excluded SNVs to output file corresponding to its allele number
with open(outFileF1, 'w') as out1, open(outFileF2, 'w') as out2, open(outFileF3, 'w') as out3:
    lastPos = ''
    second = False
    for id in sorted(excludedSNVs):
        pos = id.split(',')[0]
        if lastPos != pos:
            out1.write(excludedSNVs[id])
            lastPos = pos
            second = False
        elif not second:
            out2.write(excludedSNVs[id])
            second = True
        else:
            out3.write(excludedSNVs[id])
            second = False

print '\nDone!\n'
