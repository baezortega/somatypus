FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y wget git python-dev vcftools g++ cmake liblzma-dev zlib1g-dev libbz2-dev libcurl3-dev libssl-dev

# Install HTSlib
RUN git clone --recursive https://github.com/samtools/htslib
RUN cd htslib && make -j$(nproc) && make install -j$(nproc)
# Add HTSlib to LD_LIBRARY_PATH
ENV LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH

# Install Platypus
RUN git clone --recursive https://github.com/gtamazian/Platypus
# Install pip for Python 2
RUN wget https://bootstrap.pypa.io/pip/2.7/get-pip.py
RUN python2 get-pip.py
# Install cpython for Python 2
RUN pip2 install cython
# Install Platypus
RUN cd Platypus && make -j$(nproc)
# Add execution permission to Platypus
RUN chmod +x /Platypus/bin/Platypus.py

# Install Somatypus
RUN git clone --recursive https://github.com/baezortega/somatypus
# Make symbolic link to somatypus/bin
RUN ln -s /Platypus/bin/Platypus.py /somatypus/src/

# Add everything to PATH
RUN PATH=$PATH:/somatypus/src:/somatypus/utils
