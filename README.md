Somatypus
=========

### A Platypus-based variant calling pipeline for cancer data

Adrian Baez-Ortega

Transmissible Cancer Group, University of Cambridge

Somatypus is an open-source pipeline that makes use of the powerful variant caller Platypus for calling germ-line and somatic SNPs and indels in sequencing data coming from a set of unpaired samples. It has been designed to offer great sensitivity and specificity, even for low-frequency somatic mutations found in cancer genomes. Although this pipeline can be applied to any kind of cancer sequence data, it is particularly useful for the processing of data obtained from many tumour samples that are closely related to each other, and which lack matched normal samples, such as transmissible cancer or metastasis data.

Somatypus has been tested on Ubuntu (14.04.4) systems, and it should behave well on any Linux distribution. It has not been tested on Mac systems, but it might work, maybe requiring some minor code modifications.

##### Somatypus does...

* Call single nucleotide polymorphisms (SNPs) and short insertions/deletions (indels) from any number of sequence alignment files (subject to memory requirements), at a probably unmatched speed.

* Filter low-quality or ambiguous variants, while preserving those variants occurring with low frequency (in very few samples) and aberrant copy number (not fitting a diploid model).

* Allow the inclusion of additional calling options for Platypus, as long as they do not override the ones used in the pipeline.

* Run seamlessly from a single command.

* Resume execution after an unexpected interruption.

##### Somatypus does not...

* Call long indels or structural variants.

* Manage samples in pairs, or differentiate between ‘tumour’ and ‘host/normal’ samples, or between germ-line and somatic variants. Identification of somatic variants must be performed downstream.

* Take into account contamination between samples. Identification of variants caused by sample contamination must be performed downstream.

* Allow a highly customised execution — unless the source code is altered.


#### Read the full documentation in [docs/Somatypus Documentation.pdf] (https://github.com/adrianbaezortega/somatypus/raw/master/docs/Somatypus%20Documentation.pdf).


---

## Licence

Copyright © 2016 Transmissible Cancer Group, University of Cambridge

Author: Adrian Baez-Ortega ([ORCID 0000-0002-9201-4420] (http://orcid.org/0000-0002-9201-4420); ab2324@cam.ac.uk)

Somatypus is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see http://www.gnu.org/licenses.


---

## Installation

(The following information can be found in the INSTALL.txt file.)

Somatypus has been designed as a set of Bash and Python scripts that do not require a real 
installation, but simply adding the software directory to the PATH environment variable, 
thus making set-up straightforward. However, it has some minimal software dependencies:

 • Python 2.6 or later (not tested on Python 3.X), including development libraries.

 • Platypus (http://www.well.ox.ac.uk/platypus), which in turn requires htslib 
   (http://www.htslib.org), which in turn requires zlib (http://zlib.net).

 • VCFtools (https://vcftools.github.io), for using the vcf-sort command.

 • The tabix package (http://sourceforge.net/projects/samtools/files/tabix), for using the 
   tabix and bgzip commands. It should come together with htslib.


For the sake of tidiness, it is advisable to create a folder called 'somatypus' in the
location where you usually install software, and install all the dependencies and the
Somatypus pipeline itself (the 'somatypus-x.x' folder) into it.


The following instructions assume that you have administrator privileges in the system 
you are using (i.e. that you can do "sudo"); otherwise, you should contact you system's
administrator. Although it should be obvious, please note that you need to replace things
like "path/to/" and "/*FULL/PATH/TO*/" with the actual path to the relevant folder.
"/*FULL/PATH/TO*/" indicates that the absolute path (beginning at "/", e.g. /home/user/...)
must be used.


The recommended installation order is:


 1. Python >=2.6
    Python is normally installed by default in most UNIX systems. However, in order to 
    run Platypus, you need to install the Python development libraries.
    On Debian or Ubuntu Linux, you can install them with:
    
        sudo apt-get install python-dev
        
    On RPM-based Linux distributions, you can install them with:
    
        sudo yum install python-devel


 2. zlib (development files)
    If you have trouble installing htslib (below), you probably need to install this first.
    On Debian or Ubuntu Linux, you can install the corresponding package with:
    
        sudo apt-get install zlib1g-dev
        
    On RPM-based Linux distributions, you can install it with:
    
        sudo yum install zlib-devel


 3. htslib
    This is necessary in order to run Platypus.
    Latest version as of April 2016: 
    https://github.com/samtools/htslib/releases/download/1.3/htslib-1.3.tar.bz2

    Once downloaded and uncompressed, you can install it with:
    
        cd path/to/htslib-x.x
        ./configure
        make
        sudo make install
    
    After this, you need to add the htslib directory to your LD_LIBRARY_PATH environment
    variable. You can do this either by editing your ~/.bashrc file with a text editor 
    (e.g. nano) and adding the following line:
    
        export LD_LIBRARY_PATH=/*FULL/PATH/TO*/htslib-x.x:$LD_LIBRARY_PATH
    
    Or just by appending the relevant line to the file with:
    
        cd path/to/htslib-x.x
        echo "export LD_LIBRARY_PATH=$PWD:\$LD_LIBRARY_PATH" >> ~/.bashrc
       
    Either way, it is then necessary to source the .bashrc file for the changes to be 
    applied:
    
        source ~/.bashrc


 4. Platypus
    This is the best and the worst part of the pipeline.
    Latest version: http://www.well.ox.ac.uk/software-download-registration

    Once downloaded and uncompressed, you can install it with:
    
        cd path/to/Platypus_x.x.x
        ./buildPlatypus.sh
    
    If installation is successful, you will see the message "Finished building Platypus".
    After this, you need to make a symbolic link to the Platypus executable file in the
    somatypus-x.x/src folder (which will be then added to the PATH variable, see below).
    
        cd path/to/Platypus_x.x.x
        ln -s $PWD/Platypus.py path/to/somatypus-x.x/src/


 5. VCFtools
    On Debian or Ubuntu Linux, you can install the corresponding package with:
    
        sudo apt-get install vcftools
        
    On RPM-based Linux distributions, you can install it with:
    
        sudo yum install vcftools
    

 6. Somatypus
    The last step is adding the Somatypus directory to your PATH environment variable, so
    that the somatypus command can be called from the command line. You can do this either
    by editing your ~/.bashrc file with a text editor (e.g. nano) and adding the line:
    
        export PATH=/*FULL/PATH/TO*/somatypus-x.x/src:$PATH
    
    Or just by appending the relevant line to the file with:
    
        cd path/to/somatypus-x.x
        echo "export PATH=$PWD/src:\$PATH" >> ~/.bashrc
       
    Either way, it is then necessary to source the .bashrc file for the changes to be 
    applied:
    
        source ~/.bashrc


Once all the dependencies and the pipeline have been installed, you should be able to run 
all of the following commands (which show the usage information of each tool):

    Platypus.py callVariants -h
    tabix
    bgzip
    vcf-sort -h
    somatypus

