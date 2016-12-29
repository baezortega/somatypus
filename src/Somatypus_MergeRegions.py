#!/usr/bin/env python

# SOMATYPUS: A PLATYPUS-BASED VARIANT CALLING PIPELINE FOR CANCER DATA
# Adrian Baez-Ortega, Transmissible Cancer Group, University of Cambridge
# 14/05/2016

# Somatypus_MergeRegions.py
# Merges 'var-regions' used for re-genotyping of indels that are missing after genotyping
# Called by genotyping()

# INPUT
# regionsFile: file with the regions in CHR:START-END format, one per line


"""
This script is used to merge the regions used for re-genotyping of indels that are 
missing after the first genotyping.
"""


import sys
import os
import re


# If not 1 arguments: print help
if len(sys.argv) != 2:
    print '\nSomatypus_MergeRegions.py: Merges the regions used for re-genotyping of indels that are'
    print '                           missing after the first genotyping.'
    print '                           Input: A file with the regions in CHR:START-END format, one per line.'
    print '                           Usage: Somatypus_MergeRegions.py /path/to/regions.txt\n'
    sys.exit(0)


script, regionsFile = sys.argv


# Compose paths to output region file
print '\nInput file: ', regionsFile
outFile = regionsFile[:-4] + '_merged.txt'
print 'Output file:', outFile


# Variable for storing original regions
regions = {}


# Read original regions
print '\nReading regions...\n'
with open(regionsFile, 'r') as input:
    for line in input:
        comp = line.strip().split(':')
        chrom = comp[0]
        start = int(comp[1].split('-')[0])
        end = int(comp[1].split('-')[1])
        if chrom in regions:
            regions[chrom].append([start, end])
        else:
            regions[chrom] = [[start, end]]


# For each unprocessed region: merge it with the regions overlapping it
with open(outFile, 'w') as out:
    for chrom in sorted(regions):
        processed = [False] * len(regions[chrom])
    
        for i in range(len(regions[chrom])):
    
            # If the region has not been used before
            if not processed[i]:
                processed[i] = True
                positions = regions[chrom][i]
            
                # Find all the overlapping regions
                for j in range(len(regions[chrom])):
                    if not processed[j]:
                        start1 = min(positions)
                        end1 = max(positions)
                        start2, end2 = regions[chrom][j]
                    
                        if (start1 >= start2 and start1 <= end2) or (end1 >= start2 and end1 <= end2) or \
                           (start2 >= start1 and start2 <= end1) or (end2 >= start1 and end2 <= end1):
                            positions = positions + regions[chrom][j]
                            processed[j] = True
                        
                newRegion = chrom + ':' + str(min(positions)) + '-' + str(max(positions))
                out.write(newRegion + '\n')
                print 'Positions', chrom, ':', positions, 'merged into', newRegion

print '\nDone\n'
