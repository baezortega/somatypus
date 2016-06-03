# SOMATYPUS: A PLATYPUS-BASED VARIANT CALLING PIPELINE FOR CANCER DATA
# Adrian Baez-Ortega, Transmissible Cancer Group, University of Cambridge
# 03/06/2016

# BasicManipulation.R
# Loads variant data extracted with ExtractVcfData.py, computes VAF, generates tumour-only
# and host (non-tumour) variant sets, and produces some basic exploratory plots.
# For this script to work, tumour samples must contain a 'T' in their sample names.
# Only SNVs are used in this example.



# Read data extracted with ExtractVcfData.py
setwd("/PATH/TO/FILES/FOLDER")
snvs.nr = read.table("Somatypus_SNVs_final_NR.txt", header=T, check.names=F)
snvs.nv = read.table("Somatypus_SNVs_final_NV.txt", header=T, check.names=F)
snvs.metadata = read.table("Somatypus_SNVs_final_Metadata.txt", header=T)



# 1) Compute VAF (nv/nr)
snvs.vaf = snvs.nv / snvs.nr
snvs.vaf[is.na(snvs.vaf)] = 0



# 2) Generate tumour-only and host (non-tumour) variant sets
# Based on tumour-host contamination analysis, we have defined a tumour-only variant as:
# a variant that is found with at least 3 reads in at least one tumour, but that is not 
# found in the set of variants with VAF>0.25 in hosts.
# We know that the variants with VAF<0.25 in hosts are mostly due to contamination from
# the matched tumour. Highly tumour-contaminated hosts and their matched tumours, as
# well as tumours without matched hosts, should be excluded from the sample set first.

# Obtain sample names, and tumour and host sample indices
samples = colnames(snvs.nv)
tumours = grepl(".*T.*", samples)
hosts = !tumours

# If you want to exclude certain samples:
# excluded = samples %in% c("Sample name 1", "Sample name 2", "Sample name 3")
# tumours = grepl(".*T.*", samples) & !excluded
# hosts = !tumours & !excluded

# First, take the variants that are not found in the set of variants with VAF>0.25 in hosts
# (Variants with VAF<0.25 in a host are likely to be contamination coming from the tumour)
# (If the variant is not present in a sample, the VAF will be 0, thus <0.25)
MIN.VAF = 0.25
not.hosts = apply(snvs.vaf[,hosts], 1, function(vaf) {
    all(vaf < MIN.VAF)
})

# Second, take the variants that are found with at least 3 supporting reads in at least one tumour
MIN.READS = 3
one.tumour = apply(snvs.nv[,tumours], 1, function(nv) {
    any(nv >= MIN.READS)
})

# Extract tumour-only variants and host variants
tumour.only.idx = not.hosts & one.tumour
tumour.only.snvs = snvs.metadata[tumour.only.idx,]
host.snvs = snvs.metadata[!tumour.only.idx,]



# 3) Take histogram showing number of samples the T-only variants are shared between

# Get number of samples in which each variant is present (≥3 reads)
num.tumours = apply(snvs.nv[tumour.only.idx, tumours], 1, function(nv) {
    sum(nv >= MIN.READS)
})
hist(num.tumours, breaks=100, col="cornflowerblue", border="white", main="Number of tumours containing each T-only variant (≥3 reads)", xlab=NULL)



# 4) Plot VAF and (log) coverage for each sample

# Move to output folder
setwd("/PATH/TO/OUTPUT/FOLDER")

for (j in 1:ncol(snvs.nv)) {
    # Create PNG file
    png(paste0(samples[j], ".png"), 1600, 800)
    par(mfrow=c(2,1))
    
    # VAF: host variants first (grey), then tumour-only variants (black)
    plot(seq_along(snvs.vaf[,j])[!tumour.only.idx], snvs.vaf[!tumour.only.idx, j], xlab="SNP index", 
         ylab="VAF", main=paste0("VAF in sample ", samples[j]), pch=20, col="gray72", cex=0.6)
    points(seq_along(snvs.vaf[,j])[tumour.only.idx], snvs.vaf[tumour.only.idx, j], pch=18, col="black", cex=0.7)
    
    # Coverage (log10): all variants
    plot(seq_along(snvs.nr[,j]), log10(snvs.nr[,j]), xlab="SNP index", ylab="log10( Coverage )", 
         main=paste0("Coverage in sample ", samples[j]), pch=20, col="gray72", cex=0.7)
    
    # Close PNG
    dev.off()
    print(j)
}
