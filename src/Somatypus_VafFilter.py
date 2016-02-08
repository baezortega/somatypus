#!/usr/bin/env python

# SOMATYPUS: A PLATYPUS-BASED VARIANT CALLING PIPELINE FOR CANCER DATA
# Adrian Baez-Ortega, Transmissible Cancer Group, University of Cambridge
# 22/01/2016

# Somatypus_VafFilter.py
# Discards variants with a VAF >0.9 in all samples from a Platypus output VCF file
# Also discards indels with any flag other than PASS, and separates SNPs and indels to two different output files
# Called by merge_filter_all()

# INPUT
# vcfFile: path to VCF file


"""
This script is used to remove consistent high-VAF SNPs from a Platypus VCFs. 
For each call, it checks if the VAF (number of reads supporting variant / total reads)
is more than 0.9 (by default) across all the samples, and in that case it discards the
variant. Also discards indels with any flag other than PASS, and separates SNPs and
indels to two different output files.
"""

import sys
import gzip
import os
import re


# VAF threshold
MAXVAF = 0.9


if len(sys.argv) != 2:
    print '\nSomatypus_VafFilter.py: Discards variants with a VAF >0.9 in all samples from a Platypus output VCF file.'
    print '                        Also discards indels with any flag other than PASS, and separates SNPs and indels.'
    print '                        *All calls in the VCF must be biallelic (no commas in the ALT column).*'
    print '                 Input: Path to VCF file.'
    print '                 Usage: Somatypus_VafFilter.py /path/to/variants.vcf\n'
    sys.exit(0)


script, vcfFile = sys.argv


# Compose path of output VCF file
outFileSNP = vcfFile[:-4] + '.VAFfilt_SNPs.vcf'
outFileInd = vcfFile[:-4] + '.VAFfilt_Indels.vcf'

print '\nInput file:     ', vcfFile
print 'Output SNPs file:   ', outFileSNP
print 'Output indels file: ', outFileInd
  


count1 = 0
count2 = 0
count3 = 0
# Read every variant in the input VCF
with open(vcfFile, 'r') as vcf, open(outFileSNP, 'w') as outSNP, open(outFileInd, 'w') as outInd:
    for line in vcf:
        if line.startswith('#'):
            outSNP.write(line)
            outInd.write(line)
        else: 
            count1 = count1 + 1
            col = line.strip().split('\t')
            ref = col[3]
            alt = col[4]
            filter = col[6]
            data = col[9:]
            # If it's an indel and has any flag other than PASS, skip
            if len(ref) == len(alt) or filter == 'PASS':
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
                        if len(ref) == len(alt):
                            outSNP.write(line)
                        else:
                            outInd.write(line)
                        break
            else:
                count3 = count3 + 1


print '\n' + str(count1 - count2 - count3) + ' high-VAF variants discarded'
print count3, 'low-quality indels discarded' 
print 'Done!\n'
