Somatypus
=========

### A Platypus-based variant calling pipeline for cancer data

Adrian Baez-Ortega, Maximilian R. Stammnitz and Elizabeth P. Murchison

Transmissible Cancer Group, University of Cambridge

Developed by A.B-O. (2016)

Somatypus is an open-source pipeline that makes use of the powerful variant caller Platypus for calling germ-line and somatic SNPs and indels in sequencing data from a set of unpaired samples. It has been designed to offer great sensitivity and specificity, even for low-frequency somatic mutations found in cancer genomes. It is applicable to any kind of cancer sequence data, although it is intended, and particularly useful, for the processing of data obtained from many tumour samples that are closely related to each other, and which lack matched normal samples, such as transmissible cancer or metastasis data, because it does not require the usual ‘normal-tumour’ sample pairing.

Somatypus has been tested on Ubuntu (14.04.3) systems, and it should behave well on any Linux distribution. It has not been tested on Mac systems, but it might work, maybe requiring some minor code modifications.

Read the full documentation [here] (https://github.com/adrianbaezortega/somatypus/raw/master/docs/Somatypus%20Documentation.pdf).

---

## Licence

Copyright © 2016 Transmissible Cancer Group, University of Cambridge

Developer: Adrian Baez-Ortega ([ORCID 0000-0002-9201-4420] (http://orcid.org/0000-0002-9201-4420); ab2324@cam.ac.uk)

Somatypus is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see http://www.gnu.org/licenses.
