# snakeFeet

Snakemake version of footloop pipeline for bisulfite read analysis

## Configuration

### Sample configuration

#### Random runs

The workflow can be run in a sort of benchmarking mode where random bisulfite converted
reads are drawn from randomly generated "chromosomes" and then mapped using the
`footloop` pipeline. This was implemented largley to get a better understanding
of how the pipeline behaves under different sequence conditions and with
different parameters. 

A basic overview of the workflow in this mode would be

1. Generate `n` chromosomes informed by the parameters specified in `config/randomReads.tsv`
2. Generate `k` random reads from each chromosome.
3. For each C nucleotide in each read randomly convert it to a T based on a given bisulfite
   conversion efficiency. 
4. Map reads and call peaks using `footloop` pipeline.
5. Preform analysis and plotting on resulting peaks.

All parameters are specified in `config/randomReads.tsv`. Each row represents one
simulated chromosome and should contain the following columns.

| Field          | Value                                                                                                                       |
| -------------- | --------------------------------------------------------------------------------------------------------------------------- |
| chromosome_id  | A unique integer or string to identify this chromosome (no spaces)                                                          |
| nickname       | Easier to remember description of this chromosome, may be shown in plots                                                    |
| num_copies     | Integer number of copies of this chromosome to generate during analysis.                                                    |
| length         | Length of chromosome in basepairs (integer)                                                                                 |
| c_content      | The proportion of C nucleotides (float)                                                                                     |
| c_spacing      | Defines how C bases are distributed throughput the chromosome sequence; options currently are `uniform`, `random` or `sin`. |
| num_reads      | Number of reads to draw from each copy of this chromosome                                                                   |
| conversion_eff | Bisulfite C -> T conversion efficiency to apply to all reads from this chromosome.                                          |


#### Experimental runs

Not implemented yet. This will be used for actual data.

### Cluster configuration

## Running the workflow

If you are on UC Davis Crick (or possibly a SLURM based cluster) from the root
directory of the repo run

```
snakemake --profile workflow/profile  --configfile workflow/config/params.yaml 
```

otherwise 

```
snakemake -j 1 --configfile workflow/config/params.yaml 
```

Or configure `workflow/profile/profile.yaml` to work with your computing
environment.

