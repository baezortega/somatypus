#!/usr/bin/env python

# SOMATYPUS: A PLATYPUS-BASED VARIANT CALLING PIPELINE FOR CANCER DATA
# Adrian Baez-Ortega, Transmissible Cancer Group, University of Cambridge
# 13/05/2016

# Somatypus_VafFilter.py
# Discards variants with a VAF >0.9 in all samples from two Platypus output VCF files
# (SNVs and indels)
# Called by merge_filter_all()

# INPUT
# snvFile: path to SNVs VCF file
# indFile: path to indels VCF file


"""
This script is used to remove consistent high-VAF SNVs from two Platypus VCFs. 
For each call, it checks if the VAF (number of reads supporting variant / total reads)
is more than 0.9 (by default) across all the samples, and in that case it discards the
variant.
"""

import sys
import os
import re


# VAF threshold
MAXVAF = 0.9


if len(sys.argv) != 3:
    print '\nSomatypus_VAFfilter.py: Discards variants with a VAF >0.9 in all samples from two Platypus output VCF files'
    print '                        (one for SNVs and one for indels).'
    print '                        *All calls in the VCF must be biallelic (no commas in the ALT column).*'
    print '                 Input: Path to VCF files.'
    print '                 Usage: Somatypus_VAFfilter.py /path/to/snvs.vcf /path/to/indels.vcf\n'
    sys.exit(0)


script, snvFile, indFile = sys.argv


# Compose path of output files
outFileSNV = snvFile[:-4] + '.VAFfilt.vcf'
outFileInd = indFile[:-4] + '.VAFfilt.vcf'

print '\nInput files:    ', snvFile
print '                ', indFile
print 'Output files:   ', outFileSNV
print '                ', outFileInd
  

countSnp1 = 0
countSnp2 = 0
countInd1 = 0
countInd2 = 0


# Read every variant in the SNVs VCF
with open(snvFile, 'r') as inSNV, open(outFileSNV, 'w') as outSNV:
    for line in inSNV:
        
        if line.startswith('#'):
            outSNV.write(line)
        
        else: 
            countSnp1 = countSnp1 + 1
            col = line.strip().split('\t')
            ref = col[3]
            alt = col[4]
            filter = col[6]
            data = col[9:]

            for record in data:
                # Extract total reads (nr) and supp. reads (nv) for computing VAF
                nr = float(record.split(':')[4])
                nv = float(record.split(':')[5])
                if nr == 0:
                    vaf = 1
                else:
                    vaf = nv / nr
                # If VAF < threshold in any sample, write to corresponding output file
                if vaf <= MAXVAF:
                    countSnp2 = countSnp2 + 1
                    outSNV.write(line)
                    break
             
print '\n' + str(countSnp1 - countSnp2) + ' high-VAF SNVs discarded'


# Read every variant in the indels VCF
with open(indFile, 'r') as inInd, open(outFileInd, 'w') as outInd:
    for line in inInd:
        
        if line.startswith('#'):
            outInd.write(line)
        
        else: 
            countInd1 = countInd1 + 1
            col = line.strip().split('\t')
            ref = col[3]
            alt = col[4]
            filter = col[6]
            data = col[9:]

            for record in data:
                # Extract total reads (nr) and supp. reads (nv) for computing VAF
                nr = float(record.split(':')[4])
                nv = float(record.split(':')[5])
                if nr == 0:
                    vaf = 1
                else:
                    vaf = nv / nr
                # If VAF < threshold in any sample, write to corresponding output file
                if vaf <= MAXVAF:
                    countInd2 = countInd2 + 1
                    outInd.write(line)
                    break
             
print str(countInd1 - countInd2) + ' high-VAF indels discarded'


print 'Done!\n'
