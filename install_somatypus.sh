# INSTALLING SOMATYPUS AND DEPENDENCIES
# Adrian Baez-Ortega
# 04/02/2016


# This script installs Somatypus and all its dependencies.
#
# Before running this script, you should:
#
#   1. FIRST OF ALL, make sure you have the correct Python dependencies by running (Ubuntu):
#        sudo apt-get update
#        sudo apt-get install python-dev libxml2-dev libxslt-dev
#
#   2. Unpack the somatypus-1.0.tgz in the directory in which you want to install the 
#      software (e.g. /home/your_user/software).
#
# Then, you need to run this install script (replace the example path with your own):
#
#   /PATH/TO/somatypus-1.0/install_somatypus.sh
#
# You will be asked for your user password at some point of the process; this is because 
# you need administratorprivileges in order to install some dependencies (more concretely, 
# for running the 'make install' commands). If you do not have administrator privileges in 
# your computer, please follow alternative instructions in the INSTALL.txt file.



# Go to the installation directory
INIDIR=$PWD
cd "$( dirname "${BASH_SOURCE[0]}" )"



# Installation of software dependencies
LIBSTR="\$LD_LIBRARY_PATH"
PATHSTR="\$PATH"

# (If you can run "Platypus.py callVariants -h", then go to step 2) 
# 1. Download and install Platypus
hash Platypus.py 2>/dev/null || {   

    echo -e "\nInstalling Platypus\n"
    wget http://www.well.ox.ac.uk/bioinformatics/Software/Platypus-latest.tgz
    tar -zxvf Platypus-latest.tgz
    rm Platypus-latest.tgz
    cd Platypus_*


    # Download and install htslib (Platypus dependency)
    wget https://github.com/samtools/htslib/releases/download/1.3/htslib-1.3.tar.bz2
    tar xvjf htslib-1.3.tar.bz2
    rm htslib-1.3.tar.bz2
    mv htslib-1.3 htslib
    cd htslib
    ./configure
    make
    sudo make install    # needs admin privileges
    LIBSTR="$PWD:$LIBSTR"
    # To try htslib: type "tabix" and "bgzip"


    # Install Platypus
    cd ..
    ./buildPlatypus.sh
    PATHSTR="$PWD:$PATHSTR"
    export PATH=$PWD:$PATH
    cd ..

}
# To try Platypus: type "Platypus.py callVariants -h"
hash Platypus.py 2>/dev/null || { echo -e "\nThere was a problem installing Platypus. If the lines above do not provide further information, please run this script line-by-line to find the problem.\n" >&2; exit 1; }



# (If you can run "tabix" and "bgzip", then go to step 3)
# 2. Download and install tabix (htslib)
hash tabix 2>/dev/null || { 

    echo -e "\nInstalling tabix (htslib)\n"
    wget https://github.com/samtools/htslib/releases/download/1.3/htslib-1.3.tar.bz2
    tar xvjf htslib-1.3.tar.bz2
    rm htslib-1.3.tar.bz2
    mv htslib-1.3 htslib
    cd htslib
    ./configure
    make
    sudo make install    # needs admin privileges
    cd ..

}    
# To try htslib: type "tabix" and "bgzip"
hash tabix 2>/dev/null || { echo -e "\nThere was a problem installing tabix. If the lines above do not provide further information, please run this script line-by-line to find the problem.\n" >&2; exit 1; }
hash bgzip 2>/dev/null || { echo -e "\nThere was a problem installing bgzip. If the lines above do not provide further information, please run this script line-by-line to find the problem.\n" >&2; exit 1; }



# (If you can run "vcf-sort -h", then go to step 4)
# 3. Install VCFtools
hash vcf-sort 2>/dev/null || {

    echo -e "\nInstalling VCFtools\n"
    wget https://github.com/vcftools/vcftools/releases/download/v0.1.14/vcftools-0.1.14.tar.gz
    tar -zxvf vcftools-0.1.14.tar.gz 
    rm vcftools-0.1.14.tar.gz
    cd vcftools-0.1.14
    ./configure
    make
    sudo make install    # needs admin privileges
    cd ..

}
# To try VCFtools: type "vcf-sort -h"
hash vcf-sort 2>/dev/null || { echo -e "\nThere was a problem installing VCFtools. If the lines above do not provide further information, please run this script line-by-line to find the problem.\n" >&2; exit 1; }


# (If you can run "Somatypus_SplitMA-MNPs.py", then skip this step)
# 4. Add Somatypus to the PATH
hash somatypus 2>/dev/null || {
    
    echo -e "\nInstalling Somatypus\n"
    PATHSTR="$PWD/src:$PWD/utils:$PATHSTR"
    export PATH=$PWD/src:$PWD/utils:$PATH
    
}
# To try Somatypus: "somatypus"
hash somatypus 2>/dev/null || { echo -e "\nThere was a problem adding the Somatypus directories to the PATH. If the lines above do not provide further information, please run this script line-by-line to find the problem.\n" >&2; exit 1; }    

echo "export LD_LIBRARY_PATH=$LIBSTR" >> ~/.profile
echo "export PATH=$PATHSTR" >> ~/.profile

cd $INIDIR
echo -e "\nInstallation completed!\nNow, type:\n\nsource ~/.profile\nsomatypus\n"

