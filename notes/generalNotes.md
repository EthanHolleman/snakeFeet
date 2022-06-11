# Random read generation

In order to test out the existing footLoop pipeline and learn more / 
quantify how it behaves part of the repo will be dedicated to generating
random bisulfite reads and then feeding them to pipeline to see what "R-loops"
it calls. Basic outline of steps will be...

1. Generate "chromosome" with specific sequence characteristics
2. Draw reads of length from chromosomes
3. Using a given bisulfite C -> T conversion efficiency select regions to
   form R-loops over. Then generate reads with C -> conversions for the chromosome.
4. Store ground truth R-loop data in tsv file for later plotting and reference.

Likely will want to generate a large number of chromosomes and a large number
of reads from each chromosomes since both will be randomly generated. Also
will need configuration tables / files for both defining chromosome characteristics
and read characteristics.

