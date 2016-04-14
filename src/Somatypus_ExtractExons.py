#!/usr/bin/env python

# SOMATYPUS: A PLATYPUS-BASED VARIANT CALLING PIPELINE FOR CANCER DATA
# Adrian Baez-Ortega, Transmissible Cancer Group, University of Cambridge
# 22/01/2016

# Somatypus_ExtractExons.py
# Extracts regions from a regions file, if they contain variants from the VCFs
# Called by prepare_genotyping() and prepare_genotyping_indelflagged()

# INPUT
# exomeFile: file with the original regions in CHR:START-END format, one per line
# allele1VCF: path to VCF with bi-allelic variants / 1st allele of multi-allelic variants
# allele2VCF: path to VCF with 2nd allele of multi-allelic variants
# allele3VCF: path to VCF with 3rd allele of multi-allelic variants
# outDir: path to (existing) output folder
# excluded: logical value indicating if the variants are indel-excluded SNPs (1) or not (0)


"""
This script is used to extract the regions from a regions file that contain variants from three
different VCF files, corresponding to: bi-allelic variants / 1st allele of multi-allelic variants;
2nd allele of multi-allelic variants; 3rd allele of multi-allelic variants. The regions are 
consequently output to 3 different files, according to the alleles they contain.
"""


import sys
import os
import re


# If not 6 arguments: print help
if len(sys.argv) != 7:
    print '\nSomatypus_ExtractExons.py: Extracts regions from a regions file, if they contain variants from the VCFs.'
    print '                           The 3 VCF files correspond to: bi-allelic variants / 1st allele of'
    print '                           multi-allelic variants; 2nd allele of multi-allelic variants; 3rd allele of'
    print '                           multi-allelic variants.'
    print '                           The regions are output to 3 different files, according to the alleles they have.'
    print '                    Input: A file with the original regions in CHR:START-END format, one per line.'
    print '                           Three VCF files.'
    print '                           Path to (existing) output folder.'
    print '                           Logical value indicating if the variants are indel-excluded SNPs (1) or not (0).'
    print '                    Usage: Somatypus_ExtractExons.py /path/to/regions.txt /path/to/var1.vcf /path/to/var2.vcf /path/to/var3.vcf /path/to/outDir <0/1>\n'
    sys.exit(0)


script, exomeFile, allele1VCF, allele2VCF, allele3VCF, outDir, excluded = sys.argv


# Compose paths to output region files
print '\nExome regions file:', exomeFile
if int(excluded) == 0:
    outFile1 = outDir +'/regions_allele1.txt'
    outFile2 = outDir +'/regions_allele2.txt'
    outFile3 = outDir +'/regions_allele3.txt'
else:
    outFile1 = outDir +'/regions_allele1_indelExcluded.txt'
    outFile2 = outDir +'/regions_allele2_indelExcluded.txt'
    outFile3 = outDir +'/regions_allele3_indelExcluded.txt'


# Variables for counting and storing selected regions (exons)
count1 = 0
count2 = 0
count3 = 0
countExon = 0
allele1 = {}
allele2 = {}
allele3 = {}


# Read positions into dictionaries
print '\nReading file:', allele1VCF
with open(allele1VCF, 'r') as vcf:
    for line in vcf:
        if not line.startswith('#'):
            col = line.strip().split('\t')
            chr = col[0]
            pos = int(col[1])
            if chr in allele1:
                allele1[chr].append(pos)
            else:
                allele1[chr] = [pos]

print 'Reading file:', allele2VCF
with open(allele2VCF, 'r') as vcf:
    for line in vcf:
        if not line.startswith('#'):
            col = line.strip().split('\t')
            chr = col[0]
            pos = int(col[1])
            if chr in allele2:
                allele2[chr].append(pos)
            else:
                allele2[chr] = [pos]

print 'Reading file:', allele3VCF, '\n'
with open(allele3VCF, 'r') as vcf:
    for line in vcf:
        if not line.startswith('#'):
            col = line.strip().split('\t')
            chrom = col[0]
            pos = int(col[1])
            if chrom in allele3:
                allele3[chrom].append(pos)
            else:
                allele3[chrom] = [pos]


# Process regions and check if they contain variants
with open(exomeFile, 'r') as exome, \
     open(outFile1, 'w') as out1, open(outFile2, 'w') as out2, open(outFile3, 'w') as out3:
    
    for exon in exome:
        print 'Processing exon', exon.strip()
        countExon = countExon + 1
        exonComp = exon.strip().split(':')
        chrom = exonComp[0]
        start = int(exonComp[1].split('-')[0])
        end = int(exonComp[1].split('-')[1])
        
        # For positions in each allele dict: add exon to output file if it contains any position
        if chrom in allele1:
            for pos in allele1[chrom]:
                if start <= pos and end >= pos:
                    out1.write(exon)
                    count1 = count1 + 1
                    print ' Found in Allele 1 VCF'
                    break
    
        if chrom in allele2:
            for pos in allele2[chrom]:
                if start <= pos and end >= pos:
                    out2.write(exon)
                    count2 = count2 + 1
                    print ' Found in Allele 2 VCF'
                    break
        
        if chrom in allele3:
            for pos in allele3[chrom]:
                if start <= pos and end >= pos:
                    out3.write(exon)
                    count3 = count3 + 1
                    print ' Found in Allele 3 VCF'
                    break


print '\n', countExon, 'exons processed'
print count1, 'exons output to file', outFile1
print count2, 'exons output to file', outFile2
print count3, 'exons output to file', outFile3
print 'Done!\n'
