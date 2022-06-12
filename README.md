# snakeFeet

Snakemake version of footloop pipeline for bisulfite read analysis

## Configuration

TODO

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

