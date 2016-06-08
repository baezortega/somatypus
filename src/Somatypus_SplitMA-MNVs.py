#!/usr/bin/env python

# SOMATYPUS: A PLATYPUS-BASED VARIANT CALLING PIPELINE FOR CANCER DATA
# Adrian Baez-Ortega, Transmissible Cancer Group, University of Cambridge
# 22/01/2016

# Somatypus_SplitMA-MNPs.py
# Splits VCF records describing MNPs and multiallelic SNVs/indels into individual records
# Called by split_calls() and merge_filter_all()

# INPUT
# vcfFile: path to VCF file

 
"""
This script is used to split VCF records describing multi-nucleotide polymorphisms (MNPs)
and multiallelic variant calls into individual variant calls on different records.
"""


import sys
import os
import re


if len(sys.argv) != 2:
    print '\nSomatypus_SplitMA-MNVs.py: Splits VCF records describing MNPs and multiallelic SNVs/indels into individual records.'
    print '                    Input: Path to VCF file.'
    print '                    Usage: Somatypus_SplitMA-MNVs.py /path/to/variants.vcf\n'
    sys.exit(0)


script, vcfFile = sys.argv


# Compose paths to temporary and definitive output files
tmpFile = vcfFile[:-4] + '.split.tmp'
outFile = vcfFile[:-4] + '.split.vcf'
print '\nInput file:  ', vcfFile
print 'Output file: ', outFile


# Firstly, split any multi-allelic variant into multiple bi-allelic variants
print '\nSplitting multi-allelic variants...'
with open(vcfFile, 'r') as vcf:
    with open(tmpFile, 'w') as out:
        count = 0
        for line in vcf:
            if line.startswith('#'):
                out.write(line)
            else:
                col = line.strip().split('\t')
                chrom = col[0]
                pos = col[1]
                theId = col[2]
                ref = col[3]
                alts = col[4].split(',')
                qual = col[5]
                filters = col[6]
                info = col[7]
                format = col[8]       
                theRest = list(col[9:])

                # Don't process bi-allellic variants for now
                if len(alts) == 1:
                    out.write(line)
        
                else:
                    count = count + 1
                    for ind, alt in enumerate(alts):
                        # Create the new info
                        infoElem = info.split(';')
                        fr = infoElem[1][3:].split(',')
                        nf = infoElem[7][3:].split(',')
                        nr = infoElem[8][3:].split(',')
                        pp = infoElem[9][3:].split(',')
                        tr = infoElem[17][3:].split(',')
                        newInfo = ';'.join([ infoElem[0], 'FR='+fr[ind], infoElem[2], infoElem[3], 
                                             infoElem[4], infoElem[5], infoElem[6], 'NF='+nf[ind],
                                             'NR='+nr[ind], 'PP='+pp[ind], infoElem[10], infoElem[11],
                                             infoElem[12], infoElem[13], infoElem[14], infoElem[15], 
                                             infoElem[16], 'TR='+tr[ind], infoElem[18], infoElem[19],
                                             'FromComplex' ])
                        
                        # Create the new theRest
                        newRest = []
                        for elem in theRest:
                            stats = elem.split(':')
                            nr = stats[4].split(',')
                            nv = stats[5].split(',')
                            # Normal cases
                            if len(nr) > ind and len(nv) > ind:
                                newRest.append(':'.join([ stats[0], stats[1], stats[2], stats[3], nr[ind], nv[ind] ]))
                            # Cases where Platypus gets no data: './.:0,0,0:0:0:0:0'
                            else:
                                newRest.append(':'.join([ stats[0], stats[1], stats[2], stats[3], nr[0], nv[0] ]))
                                
                        newLine = '\t'.join([ chrom, pos, theId, ref, alt, qual, filters, 
                                              newInfo, format, '\t'.join(newRest) ])    
                        out.write(newLine + '\n')

print count, 'multi-allelic variants found'


# Secondly, split MNPs into SNVs
print 'Splitting MNPs...'
with open(tmpFile, 'r') as vcf:
    with open(outFile, 'w') as out:
        count = 0
        for line in vcf:
            if line.startswith('#'):
                out.write(line)
            else:
                col = line.strip().split('\t')
                chrom = col[0]
                pos = col[1]
                theId = col[2]
                ref = col[3]
                alt = col[4]
                qual = col[5]
                filters = col[6]
                info = col[7]
                format = col[8]       
                theRest = '\t'.join(col[9:])

                # Check that the record is not a SNV or an indel
                if len(ref) != len(alt) or len(ref) == 1:
                    out.write(line)
                else:
                    count = count + 1
                    for ind, (refBase, altBase) in enumerate(zip(ref, alt)):
                        if refBase != altBase:
                            newPos = str(int(pos) + ind)
                            newLine = '\t'.join([ chrom, newPos, theId, refBase, altBase, qual, filters, 
                                                  info, format, theRest ])
                            out.write(newLine + '\n')


print count, 'MNPs found'
os.remove(tmpFile)
print 'Done!\n'
