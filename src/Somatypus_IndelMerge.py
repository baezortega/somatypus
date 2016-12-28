#!/usr/bin/env python

# SOMATYPUS: A PLATYPUS-BASED VARIANT CALLING PIPELINE FOR CANCER DATA
# Adrian Baez-Ortega, Transmissible Cancer Group, University of Cambridge
# 22/01/2016

# Somatypus_IndelMerge.py
# Extracts indels from multiple Platypus output VCF files
# Called by extract_indels()

# INPUT
# inputFile: text file with paths to VCF files, one per line
# outDir: path to (existing) output folder


"""
This script is used to extract indels from multiple Platypus VCFs. In each VCF, it selects 
only bi-allelic indels without any of the flags badReads, MQ, strandBias, SC, or QD, 
and merges them into a set of indels, which is output to a new VCF file.
"""


import sys
import os
import re


# If not 2 arguments: print help
if len(sys.argv) != 3:
    print '\nSomatypus_IndelMerge.py: Extracts indels from multiple Platypus output VCF files.'
    print '                         *The VCFs need to be as they are output by Platypus (unsplit calls).*'
    print '                         For each VCF, it selects only bi-allelic indels without any of the'
    print '                         flags: badReads, MQ, strandBias, SC, or QD.'
    print '                         It ensures that no two indels share position in different samples.'
    print '                  Input: A text file with paths to VCF files, one per line.'
    print '                         Path to (existing) output folder.'
    print '                  Usage: Somatypus_IndelMerge.py /path/to/fileList.txt /path/to/outDir\n'
    sys.exit(0)


script, inputFile, outDir = sys.argv


# Extract indels from each sample
indels = {}
with open(inputFile, 'r') as vcfList:
    for listLine in vcfList:
        vcfFile = listLine.strip()
        print 'Extracting indels from file ' + vcfFile
        with open(vcfFile, 'r') as vcf:
            for line in vcf:
                if not line.startswith('#'):
                    col = line.strip().split('\t')
                    chrom = col[0]
                    pos = col[1]
                    ref = col[3]
                    alt = col[4]
                    filter = col[6]
                    # Look for bi-allelic indels without flags badReads, MQ, strandBias, SC, or QD
                    if ',' not in alt and len(ref) != len(alt) \
                      and 'badReads' not in filter and 'MQ' not in filter and 'strandBias' not in filter and 'SC' not in filter and 'QD' not in filter:
                        id = chrom + ':' + pos + ',' + ref + '>' + alt
                        if id not in indels:
                            indels[id] = line


# Discard multi-allelic calls that never occur together but are on the same position
mergedIndels = {}
for id in indels:
    # Extract CHR:POS, and group indels according to it
    location = id.split(',')[0]
    if location in mergedIndels:
        mergedIndels[location].append(indels[id])
    else:
        mergedIndels[location] = [indels[id]]


# Write merged indels to output file
outFile = outDir + '/MergedIndels.vcf'
print '\nMerging indels into file ' + outFile

with open(outFile, 'w') as out:
    for loc in sorted(mergedIndels):
        # Omit entries (positions) with more than one element (indel)
        if len(mergedIndels[loc]) == 1:
            out.write(mergedIndels[loc][0])

print 'Done!\n'
