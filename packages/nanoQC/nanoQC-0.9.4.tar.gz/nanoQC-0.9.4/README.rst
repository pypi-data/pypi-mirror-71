nanoQC
======

Quality control tools for long read sequencing data aiming to replicate
some of the plots made by fastQC. This is an immature tool and I welcome
all contributions.

|Twitter URL| |install with conda|

Creates dynamic plots using
`bokeh <https://bokeh.pydata.org/en/latest/>`__. For an example see
`here <http://decoster.xyz/wouter/>`__

INSTALLATION
------------

.. code:: bash

   pip install nanoQC

| or
| |install with conda|

::

   conda install -c bioconda nanoqc

USAGE
-----

::

   nanoQC [-h] [-v] [-o OUTDIR] fastq

   positional arguments:
     fastq                 Reads data in fastq.gz format.

   optional arguments:
     -h, --help            show this help message and exit
     -v, --version         Print version and exit.
     -o, --outdir OUTDIR   Specify directory in which output has to be created.
     -l, --minlen int      Minimum length of reads to be included in the plots
                           This also controls the length plotted in the graphs
                           from the beginning and end of reads (length plotted = minlen / 2)

CITATION
--------

If you use this tool, please consider citing our
`publication <https://academic.oup.com/bioinformatics/advance-article/doi/10.1093/bioinformatics/bty149/4934939>`__.

CONTRIBUTIONS
-------------

Thanks to: - Jasper Ouwerkerk
(`JasperO98 <https://github.com/JasperO98>`__) for improving how reads
are selected (v0.8.0)

.. |Twitter URL| image:: https://img.shields.io/twitter/url/https/twitter.com/wouter_decoster.svg?style=social&label=Follow%20%40wouter_decoster
   :target: https://twitter.com/wouter_decoster
.. |install with conda| image:: https://anaconda.org/bioconda/nanoqc/badges/installer/conda.svg
   :target: https://anaconda.org/bioconda/nanoqc
