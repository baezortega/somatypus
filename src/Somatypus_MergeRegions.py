#!/usr/bin/env python

# SOMATYPUS: A PLATYPUS-BASED VARIANT CALLING PIPELINE FOR CANCER DATA
# Adrian Baez-Ortega, Transmissible Cancer Group, University of Cambridge
# 14/05/2016
# Updated by Kevin Gori, 26/01/2017

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
from collections import defaultdict


# If not 1 arguments: print help
if len(sys.argv) != 2:
    print ('\nSomatypus_MergeRegions.py: Merges the regions used for re-genotyping of indels that are')
    print ('                           missing after the first genotyping.')
    print ('                           Input: A file with the regions in CHR:START-END format, one per line.')
    print ('                           Usage: Somatypus_MergeRegions.py /path/to/regions.txt\n')
    sys.exit(0)


script, regionsFile = sys.argv


# Compose paths to output region file
print ('\nInput file: ', regionsFile)
outFile = regionsFile[:-4] + '_merged.txt'
print ('Output file:', outFile)


# Variable for storing original regions
regions = defaultdict(list)


# Read original regions
print ('\nReading regions...\n')
with open(regionsFile, 'r') as input_:
    for line in input_:
        if line == '\n': continue
        chrom, start_end = line.strip().split(':')
        start, end = start_end.split('-')
        regions[chrom].append([int(start), int(end)])

chroms = sorted(regions)


# For each unprocessed region: merge it with the regions overlapping it
with open(outFile, 'w') as out:
    for chrom in chroms:
        # sort regions list by ascending starts, so never have to deal with overlaps below the current region
        regions[chrom].sort()

        # don't do work on empty list
        if len(regions[chrom]) == 0:
            continue

        merged_region = regions[chrom][0]
        positions = merged_region[:] # this is only used so terminal output is the same as original version

        for test_region in regions[chrom][1:]:
            # If test_region starts before the active merged_region ends, then we know they overlap
            if test_region[0] <= merged_region[1]:
                # Removed an assertion here that wasn't true - KG Jan 2020

                # update the end of the merged region if test region end is beyond it, and the positions
                merged_region[1] = max(merged_region[1], test_region[1])
                positions.extend(test_region)
            else:
                # new region doesn't overlap, so let's pack up and move on
                out.write('{}:{}-{}\n'.format(chrom, merged_region[0], merged_region[1]))
                print('Positions {0} : {1} merged into {0}:{2}-{3}'.format(chrom, positions, merged_region[0],
                                                                           merged_region[1]))
                merged_region = test_region
                positions = merged_region[:]

        # Don't forget to output the final merged region
        out.write('{}:{}-{}\n'.format(chrom, merged_region[0], merged_region[1]))
        print('Positions {0} : {1} merged into {0}:{2}-{3}'.format(chrom, positions, merged_region[0],
                                                                   merged_region[1]))

print ('\nDone\n')
