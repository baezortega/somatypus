#!/usr/bin/env python

# SOMATYPUS: A PLATYPUS-BASED VARIANT CALLING PIPELINE FOR CANCER DATA
# Adrian Baez-Ortega, Transmissible Cancer Group, University of Cambridge
# 22/01/2016

# Somatypus_IndelRescuedFilter.py
# Discards rescued indel-flagged SNVs with median read coverage <20, median VAF <0.2 or median VAF >0.9
# Called by merge_filter_indelflagged()

# INPUT
# vcfFile: path to VCF file with genotyped indel-flagged variants


"""
This script is used to remove SNVs with median read coverage <20, median VAF <0.2 or 
median VAF >0.9 from a Platypus VCFs. For each call, it checks if the median read coverage 
and median VAF (number of reads supporting variant / total reads) are inside the defined, 
threshold (COV=20, VAF=0.2-0.9) and otherwise it discards the variant. Median VAF is 
computed only in samples with at least 3 reads supporting the variant.
"""


import sys
import os
import re


# If not 1 argument: print help
if len(sys.argv) != 2:
    print '\nSomatypus_IndelRescuedFilter.py: Discards SNVs with median read coverage <20, median VAF <0.2 or median VAF >0.9'
    print '                                 from a Platypus output VCF file.'
    print '                                 Median VAF is computed only in samples with >2 reads supporting the variant.'
    print '                                 This script is intended to be used on the variants flagged by the indel filter,'
    print '                                 genotyped separatedly and quality-filtered.'
    print '                          Input: Path to VCF file containing genotyped indel-flagged variants.'
    print '                          Usage: Somatypus_IndelRescuedFilter.py /path/to/variants.vcf\n'
    sys.exit(0)


script, vcfFile = sys.argv


# Coverage and VAF thresholds
MINCOV = 20
MINVAF = 0.2
MAXVAF = 0.9
# Minimum number of supp. reads for contributing to median VAF
MINREADS = 3


# Function for computing median
def median(l):
    if len(l) > 1:
        half = len(l) // 2
        l.sort()
        if not len(l) % 2:
            return (l[half - 1] + l[half]) / 2.0
        return l[half]
    elif len(l) == 1:
        return l[0]
    else:
        return None


# Compose path to output VCF file
outFile = vcfFile[:-4] + '.VAFfilt.vcf'
print '\nInput file:  ', vcfFile
print 'Output file: ', outFile  


# Extract SNVs from each sample, if they are not in the exclude list
count1 = 0
count2 = 0
with open(vcfFile, 'r') as vcf, open(outFile, 'w') as out:
    for line in vcf:
        if line.startswith('#'):
            out.write(line)
        else:
            count1 = count1 + 1
            vaf = []
            cov = []
            # Extract sample data
            data = line.strip().split('\t')[9:]
            for record in data:
                # Extract total reads (nr) and supp. reads (nv)
                nr = float(record.split(':')[4])
                nv = float(record.split(':')[5])
                # Add coverage and VAF values to list
                cov.append(nr)
                if nv >= MINREADS:
                    vaf.append(nv / nr)
                    
            # If coverage and VAF values are not beyond thresholds, write to output
            if median(cov) >= MINCOV and median(vaf) >= MINVAF and median(vaf) <= MAXVAF:
                count2 = count2 + 1
                out.write(line)
                
                
print '\n' + str(count1 - count2) + ' variants discarded'
print 'Done!\n'
