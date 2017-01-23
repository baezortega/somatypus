#### Download the latest release: Somatypus 1.3  ( [zip](../../archive/v1.3.zip) | [tar.gz](../../archive/v1.3.tar.gz) ).

---


Somatypus
=========

### A Platypus-based variant calling pipeline for cancer data

__Adrian Baez-Ortega  
Transmissible Cancer Group, University of Cambridge__

Somatypus is an open-source pipeline that makes use of the powerful variant caller Platypus for identifying germline and somatic SNVs and indels in sequencing data coming from a set of unpaired samples. It has been designed to offer great sensitivity and specificity, even for low-frequency somatic mutations found in cancer genomes. Although this pipeline can be applied to any cancer sequence data, it is particularly useful for the processing of data obtained from many tumour samples that are closely related to each other and lack matched normal samples, such as transmissible cancer or metastasis data.

Somatypus has been tested on Ubuntu (14.04.4) systems, and it should work well on any Linux distribution. It has not been tested on Mac systems, although it may work after some minor code modifications.


#### Somatypus does...

* Call single nucleotide variants (SNVs) and short insertions/deletions (indels) from any number of sequence alignment files (subject to memory constraints), at a probably unmatched speed.

* Filter low-quality or ambiguous variants, while keeping those variants occurring with low frequency (in a few samples) or aberrant copy number (not fitting a diploid model).

* Allow the use of additional calling options for Platypus, as long as they do not override the ones defined in the pipeline.

* Run seamlessly from a single command.

* Resume execution after an unexpected interruption.

#### Somatypus does not...

* Call long indels, structural variants or copy number changes.

* Manage samples in pairs, or distinguish between “tumour” and “host/normal” samples (or between germline and somatic variants). Identification of somatic variants must be performed downstream.

* Take into account cross-sample contamination. Identification of variants caused by contamination must be performed downstream.

* Allow extensive workflow customisation (unless the source code is altered).


---

## Installation

(The following information can be found in the INSTALL.txt file.)

Somatypus has been designed as a set of Bash and Python scripts that do not require a real 
installation, but simply adding the software directory to the PATH environment variable, 
thus making set-up straightforward. However, it has some minimal software dependencies:

* __Python 2.6 or later__ (not tested on Python 3.X), including development libraries.

* __Platypus__ (http://www.well.ox.ac.uk/platypus), which in turn requires __htslib__ (http://www.htslib.org), which in turn requires __zlib__ (http://zlib.net).

* __VCFtools__ (https://vcftools.github.io), for using the vcf-sort command.

* The __tabix__ package (http://sourceforge.net/projects/samtools/files/tabix), for using the tabix and bgzip commands. It should come together with htslib.


For the sake of tidiness, it is advisable to create a folder called "somatypus" in the
location where you usually install software, and install all the dependencies and the
Somatypus pipeline itself (the somatypus-x.x folder) into it.


The following instructions assume that you have administrator privileges in the system 
you are using (i.e. that you can do "sudo"); otherwise, you should contact you system's
administrator. __Although it should be obvious, please note that you need to replace
things like "path/to/" and "/FULL/PATH/TO/" with the actual path to the relevant folder.
"/FULL/PATH/TO/" indicates that the absolute path (beginning at "/", e.g. /home/user/...)
must be used.__


The recommended installation order is:


 1. __Python ≥2.6__
 
    Python is normally installed by default in most UNIX systems. However, in order to run Platypus, you need to install the Python development libraries.  
    On Debian or Ubuntu Linux, you can install them with:
        
        sudo apt-get install python-dev
    
    On RPM-based Linux distributions, you can install them with:

        sudo yum install python-devel


 2. __zlib (development files)__
 
    If you have trouble installing htslib (below), you probably need to install this first.  
    On Debian or Ubuntu Linux, you can install the corresponding package with:

        sudo apt-get install zlib1g-dev
    
    On RPM-based Linux distributions, you can install it with:

        sudo yum install zlib-devel


 3. __htslib__
 
    This is necessary in order to run Platypus.  
    Latest version as of April 2016: https://github.com/samtools/htslib/releases/download/1.3/htslib-1.3.tar.bz2  
    Once downloaded and uncompressed, you can install it with:

        cd path/to/htslib-x.x
        ./configure
        make
        sudo make install

    After this, you need to add the htslib directory to your LD_LIBRARY_PATH environment variable. You can do this either by editing your ~/.bashrc file with a text editor (e.g. nano) and adding the following line:

        export LD_LIBRARY_PATH=/FULL/PATH/TO/htslib-x.x:$LD_LIBRARY_PATH

    Or just by appending the relevant line to the file with:

        cd path/to/htslib-x.x
        echo "export LD_LIBRARY_PATH=$PWD:\$LD_LIBRARY_PATH" >> ~/.bashrc
   
    Either way, it is then necessary to source the .bashrc file for the changes to be applied:

        source ~/.bashrc


 4. __Platypus__
 
    This is the best and the worst part of the pipeline.  
    Latest version: http://www.well.ox.ac.uk/software-download-registration  
    Once downloaded and uncompressed, you can install it with:

        cd path/to/Platypus_x.x.x
        ./buildPlatypus.sh

    If installation is successful, you will see the message "Finished building Platypus". After this, you need to make a symbolic link to the Platypus executable file in the somatypus-x.x/src folder (which will be then added to the PATH variable, see below).

        cd path/to/Platypus_x.x.x
        ln -s $PWD/Platypus.py path/to/somatypus-x.x/src/


 5. __VCFtools__
 
    On Debian or Ubuntu Linux, you can install the corresponding package with:

        sudo apt-get install vcftools
    
    On RPM-based Linux distributions, you can install it with:

        sudo yum install vcftools
    

 6. __Somatypus__
 
    The last step is adding the Somatypus directory to your PATH environment variable, so that the somatypus command can be called from the command line. You can do this either by editing your ~/.bashrc file with a text editor (e.g. nano) and adding the line:

        export PATH=/FULL/PATH/TO/somatypus-x.x/src:/FULL/PATH/TO/somatypus-x.x/utils:$PATH

    Or just by appending the relevant line to the file with:

        cd path/to/somatypus-x.x
        echo "export PATH=$PWD/src:$PWD/utils:\$PATH" >> ~/.bashrc
   
    Either way, it is then necessary to source the .bashrc file for the changes to be applied:
    
        source ~/.bashrc


Once all the dependencies and the pipeline have been installed, you should be able to run all of the following commands (which show the usage information of each tool):

    Platypus.py callVariants -h
    tabix
    bgzip
    vcf-sort -h
    somatypus

And now you can have fun.


---

## Running Somatypus

When the pipeline is run via the `somatypus` command with no options (or with `-h`), it displays the usage information.

    | SOMATYPUS
    | A Platypus-based variant calling pipeline for cancer data
    | Version x.x
    |
    | Required input:
    |    -i  Absolute path to folder containing the input BAM files (accompanied by BAI indices).
    |    -g  Absolute path to reference genome FASTA file (accompanied by FAI index).
    |    -o  Absolute path to the output folder (it will be created if needed).
    |
    | Optional input:
    |    -r  Absolute path to file of regions to use, one per line in CHR:START-END format.
    |    -c  Number of CPUs (processes) for Platypus *(should not exceed 8 due to a bug)*.
    |    -p  Additional options for Platypus, within quotes and separated by spaces.
    |
    | Options:
    |    -d  Disable use of regions around the variants during genotyping (incompatible with -r).
    |    -h  Print this usage information and exit.
    |    -v  Print version and exit.
    |
    | Usage:
    |    somatypus -i /path/to/bams_dir -o /path/to/out_dir -g /path/to/genome.fna -r /path/to/regions.txt -c <1-8> -p "--option=VAL --option=VAL"	

It is advisable that all the input paths be absolute, rather than relative. An optional regions file allows the user to define a set of genomic regions (e.g. exons) wherein to perform the calling. The regions file must be a text file containing one region per line, in CHR:START-END format (e.g. 1:1028676-1028844. The chromosome labels must match those in the reference FASTA and in the sample BAMs). 

If no regions file is provided, regions of +/-200 bp around each variant will be defined during genotyping, in order to increase efficiency. This behaviour can be disabled via the `-d` option (which is incompatible with `-r`).

The number of CPUs is also optional (default is 1) but, if specified, must be at least 1, and should not exceed 8 (or even less, depending on the amount of data), due to an inveterate Platypus bug that can cause an extremely excessive memory allocation attempt (see the [full documentation](docs/Somatypus%20Documentation.pdf)).

Finally, additional calling options can be passed to Platypus via the `-p` option. The entire additional options string must be quoted, and options must be separated by spaces. However, those options already specified in the pipeline cannot be included, namely: `--logFileName`, `--refFile`, `--bamFiles`, `--regions`, `--minPosterior`, `--minReads`, `--minFlank`, `--trimReadFlank`, `--source`, `--getVariantsFromBAMs`, `--nCPU`, or `--output` (or `-o`). (For obvious reasons, they should also not include `--help` or `-h`.)

A list of all the Platypus options can be consulted via: `Platypus.py callVariants -h`.

The full log of the pipeline execution will be stored in a file named SOMATYPUS_<*date+time*>.log, in the logs subfolder of the output directory, together with the logs of most of the steps. The log files and the temporary folders containing intermediate files will be numbered according to the number of the steps that interact with them.


### For more information on the workflow and output files, please read the full documentation in [docs/Somatypus Documentation.pdf](docs/Somatypus%20Documentation.pdf).


---

## Licence

Copyright © 2016 Transmissible Cancer Group, University of Cambridge  
Author: Adrian Baez-Ortega ([ORCID 0000-0002-9201-4420] (http://orcid.org/0000-0002-9201-4420); ab2324@cam.ac.uk)

Somatypus is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see http://www.gnu.org/licenses.
