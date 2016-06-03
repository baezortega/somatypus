#!/usr/bin/env python

# SOMATYPUS: A PLATYPUS-BASED VARIANT CALLING PIPELINE FOR CANCER DATA
# Adrian Baez-Ortega, Transmissible Cancer Group, University of Cambridge
# 09/02/2016

# ExtractVcfData.py
# Extracts metadata, NR and NV values from a Platypus VCF into three text files

# INPUT
# vcfFile: path to input VCF file


"""
This script is used to extract the metadata (CHROM, POS, ID, REF, ALT, QUAL, FILTER, INFO), 
the total number of reads (NR) and the number of reads supporting the variant (NV), from 
every variant in a VCF file, into three respective output text files. 
"""


import sys
import gzip
import os
import re


# If not 1 argument: print help
if len(sys.argv) != 2:
    print '\nExtractVcfData.py: Extracts the metadata (CHROM, POS, ID, REF, ALT, QUAL, FILTER, INFO), the'
    print '                   total number of reads (NR) and the number of reads supporting the variant (NV),'
    print '                   from every variant in a VCF file, into three respective output text files.'
    print '            Input: Path to input VCF file.'
    print '            Usage: ExtractVcfData.py /path/to/file.vcf\n'
    sys.exit(0)


script, vcfFile = sys.argv

# Compose path to output VCF file
outFileNR = vcfFile[:-4] + '_NR.txt'
outFileNV = vcfFile[:-4] + '_NV.txt'
outFileMD = vcfFile[:-4] + '_Metadata.txt'
print '\nInput file: ', vcfFile
print 'Output NR file: ', outFileNR
print 'Output NV file: ', outFileNV
print 'Output metadata file: ', outFileMD



with open(vcfFile, 'r') as vcf, open(outFileNR, 'w') as outNR, open(outFileNV, 'w') as outNV, open(outFileMD, 'w') as outMD:
    i = 0
    for line in vcf:
        i = i + 1
        # Skip first 47 header lines, and write column headers
        if i == 48:
            MDhead = line[1:].strip().split('\t')[:8]
            NRhead = line.strip().split('\t')[9:]
            outMD.write('\t'.join(MDhead) + '\n')
            outNR.write('\t'.join(NRhead) + '\n')
            outNV.write('\t'.join(NRhead) + '\n')
            
        elif i > 48:
            # Extract metadata
            metadata = line.strip().split('\t')[:8]
            outMD.write('\t'.join(metadata) + '\n')
            
            # Extract NR and NV from sample data
            NR = []
            NV = []
            data = line.strip().split('\t')[9:]
            for record in data:
                # Extract total reads (nr) and supp. reads (nv)
                nr = record.split(':')[4]
                nv = record.split(':')[5]
                # Add coverage and VAF values to list
                NR.append(nr)
                NV.append(nv)
                
            outNR.write('\t'.join(NR) + '\n')
            outNV.write('\t'.join(NV) + '\n')
            
                
print 'Done!\n'

