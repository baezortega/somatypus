#!/usr/bin/env python

# SOMATYPUS: A PLATYPUS-BASED VARIANT CALLING PIPELINE FOR CANCER DATA
# Adrian Baez-Ortega, Transmissible Cancer Group, University of Cambridge
# 2016-2017

# Somatypus_VafFilter.py
# Discards variants with a VAF >0.9 in all samples from a Platypus output VCF file
# Called by merge_filter_all()

# INPUT
# vcfFile: path to VCF file


"""
This script is used to remove consistent high-VAF variants from a Platypus VCF. 
For each call, it checks if the VAF (number of reads supporting variant / total reads)
is more than 0.9 (by default) across all the samples, and in that case it discards the
variant.
"""

import sys
import os
import re


# VAF threshold
MAXVAF = 0.9


if len(sys.argv) != 2:
    print '\nSomatypus_VAFfilter.py: Discards variants with a VAF >0.9 in all samples from a Platypus output VCF file'
    print '                        *All calls in the VCF must be biallelic (no commas in the ALT column).*'
    print '                 Input: Path to VCF file.'
    print '                 Usage: Somatypus_VAFfilter.py /path/to/variants.vcf\n'
    sys.exit(0)


script, vcfFile = sys.argv


# Compose path of output files
outFile = vcfFile[:-4] + '.VAFfilt.vcf'

print '\nInput file:  ', vcfFile
print 'Output file: ', outFile
  

count1 = 0
count2 = 0


# Read every variant in the SNVs VCF
with open(vcfFile, 'r') as input, open(outFile, 'w') as output:
    for line in input:
        
        if line.startswith('#'):
            output.write(line)
        
        else: 
            count1 = count1 + 1
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
                    count2 = count2 + 1
                    output.write(line)
                    break
             
print '\n' + str(count1 - count2) + ' high-VAF variants discarded'

print 'Done\n'
