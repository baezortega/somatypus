#!/usr/bin/env python

# SOMATYPUS: A PLATYPUS-BASED VARIANT CALLING PIPELINE FOR CANCER DATA
# Adrian Baez-Ortega, Transmissible Cancer Group, University of Cambridge
# 22/01/2016

# Somatypus_IndelFlag.py
# Identifies SNVs close to indels in multiple Platypus output VCF files
# Called by indel_flag()

# INPUT
# inputFile: text file with paths to VCF files, one per line
# outFile: path to output file


"""
This script is used to extract the coordinates and variant bases of SNVs which are too close 
to an indel in any sample, from multiple Platypus VCFs, and write them into an output file.
"""


import sys
import os
import re
from sets import Set


# If not 2 arguments: print help
if len(sys.argv) != 3:
    print '\nSomatypus_IndelFlag.py: Identifies SNVs close to indels in multiple Platypus output VCF files.'
    print '                        *The VCFs need to be split first with the splitMAandMNPs.py script.*'
    print '                        For each VCF, it extracts the coordinates of the bases up to 5bp'
    print '                        upstream and downstream any indel; then, it detects SNVs inside'
    print '                        these regions in the same sample and outputs them into a text file.'
    print '                 Input: A text file with paths to VCF files, one per line.'
    print '                        Path to output file.'
    print '                 Usage: Somatypus_IndelFlag.py /path/to/fileList.txt /path/to/outFile.txt\n'
    sys.exit(0)


# Number of bases to exclude at each side of an indel footprint
WINDOW = 5


script, inputFile, outFile = sys.argv
flaggedSNVs = Set([])


# Extract SNVs near indels from each sample
with open(inputFile, 'r') as vcfList:
    for listLine in vcfList:
        vcfFile = listLine.strip()
        print 'Processing file ' + vcfFile
        
        # First: mark positions covered by indels
        indelPos = Set([])
        with open(vcfFile, 'r') as vcf:
            for line in vcf:
                if not line.startswith('#'):
                    col = line.strip().split('\t')
                    chrom = col[0]
                    pos = col[1]
                    ref = col[3]
                    alt = col[4]
                    if ',' in alt:
                        print '\nERROR: Multiallelic variant found at ' + chrom + ':' + pos + '. Use splitMAandMNPs.py first.\n'
                        sys.exit(1)
                    # If indel, mark a window of WINDOW bp at both flanks of the indel position/footprint
                    if len(ref) != len(alt):
                        # If deletion: footprint is the length of the REF, only downstream
                        if len(ref) > len(alt):
                            ftprint = len(ref) - 1
                        else:
                            ftprint = 0
                        for position in range(int(pos) - WINDOW, int(pos) + ftprint + WINDOW + 1):
                            indelPos.add(chrom + ':' + str(position))

        # Second: extract SNVs overlapping indels
        with open(vcfFile, 'r') as vcf:
            for line in vcf:
                if not line.startswith('#'):
                    col = line.strip().split('\t')
                    chrom = col[0]
                    pos = col[1]
                    ref = col[3]
                    alt = col[4]

                    # For each SNV: check if it's near an indel
                    if len(ref) == len(alt):
                        location = chrom + ':' + pos
                        if len(ref) != 1:
                            print '\nERROR: MNP found at ' + location + '. Use splitMAandMNPs.py first.\n'
                            sys.exit(1) 
                        # If near an indel: add to flaggedSNVs set
                        if location in indelPos:
                            id = chrom + ':' + pos + ',' + ref + '>' + alt
                            flaggedSNVs.add(id)


# Write flagged SNVs from all files to output file
print 'Writing indel-flagged SNVs to ' + outFile
with open(outFile, 'w') as out:
    for snv in sorted(flaggedSNVs):
        out.write(snv + '\n')


print 'Done!\n'
