set -ev

git clone https://github.com/wdecoster/nanotest.git

nanoQC -h
nanoQC nanotest/reads.fastq.gz
nanoQC nanotest/reads.fastq.gz --minlen 100
