NANOPACK
========

Easily install all my long read processing and analysis scripts
simultaneously.

Installation
------------

``pip install nanopack`` ## Updating ``pip install nanopack --upgrade``

These scripts are written and tested for Python3, and may not work on
Python2.

Content
-------

Scripts
~~~~~~~

`NanoPlot <https://github.com/wdecoster/NanoPlot>`__: creating many
relevant plots derived from reads (fastq), alignments (bam) and albacore
summary files. Examples can be found in `the gallery on my
blog <https://gigabaseorgigabyte.wordpress.com/2017/06/01/example-gallery-of-nanoplot/>`__.
NanoPack is also available with a graphical user interface in
`NanoGUI <https://github.com/wdecoster/nanogui>`__ or as a `web
service <http://nanoplot.bioinf.be>`__.

`NanoComp <https://github.com/wdecoster/nanocomp>`__: comparing multiple
runs on read length and quality based on reads (fastq), alignments (bam)
or albacore summary files.

`NanoQC <https://github.com/wdecoster/nanoQC>`__: Generating plots to
investigate nucleotide composition and quality distribution at the end
of reads.

`NanoStat <https://github.com/wdecoster/nanostat>`__: Quickly create a
statistical summary from reads, an alignment or a summary file.

`NanoFilt <https://github.com/wdecoster/nanofilt>`__: Streaming script
for filtering a fastq file based on a minimum length, minimum quality
cut-off, minimum and maximum average GC. Also trimming nucleotides from
either read ends is an option.

`NanoLyse <https://github.com/wdecoster/nanolyse>`__: Streaming script
for filtering a fastq file to remove reads mapping to the lambda phage
genome (control DNA used in nanopore sequencing). Uses
`minimap2/mappy <https://github.com/lh3/minimap2>`__.

Modules
~~~~~~~

`nanoget <https://github.com/wdecoster/nanoget>`__: Functions for
extracting features from reads, alignments and albacore summary data,
parallelized.

`nanomath <https://github.com/wdecoster/nanomath>`__: Functions for
mathematical processing and calculating statistics.

Test data
~~~~~~~~~

`nanotest <https://github.com/wdecoster/nanotest>`__ provides small test
datasets in fastq, bam and summary format (not included when installing
NanoPack)

## CITATION If you use this tool, please consider citing our
`publication <https://academic.oup.com/bioinformatics/advance-article/doi/10.1093/bioinformatics/bty149/4934939>`__.
