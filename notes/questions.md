# Footloop pipeline questions

## `footLoop.pl`

### General questions

- What should be included in the `-i` (index argument)?
  - Seems like just a bed6 file with gene annotations for the "genome" you are
    mapping to. For simulated reads just generating a dummy gene that spans the
    length of the chromosome.
- What is `-l` (label) used for?

### Errors

- Running bismark is successful and seems like all output is being generated. Output of `tree -a`
  in the output directory below.
  ```

    ├── BED-c0-3.bed_0_0_bp.bed
    ├── .bismark_log
    ├── .geneIndex
    │   └── a0a5052043f6c374eed31d7f6ca449b4
    │       ├── BED-c0-3.bed_0_0_bp.bed.fa
    │       ├── .BED-c0-3.bed_0_0_bp.bed.fa.md5
    │       ├── Bisulfite_Genome
    │       │   ├── CT_conversion
    │       │   │   ├── BS_CT.1.bt2
    │       │   │   ├── BS_CT.2.bt2
    │       │   │   ├── BS_CT.3.bt2
    │       │   │   ├── BS_CT.4.bt2
    │       │   │   ├── BS_CT.rev.1.bt2
    │       │   │   ├── BS_CT.rev.2.bt2
    │       │   │   └── genome_mfa.CT_conversion.fa
    │       │   ├── GA_conversion
    │       │   │   ├── BS_GA.1.bt2
    │       │   │   ├── BS_GA.2.bt2
    │       │   │   ├── BS_GA.3.bt2
    │       │   │   ├── BS_GA.4.bt2
    │       │   │   ├── BS_GA.rev.1.bt2
    │       │   │   ├── BS_GA.rev.2.bt2
    │       │   │   └── genome_mfa.GA_conversion.fa
    │       │   └── .md5sum
    │       └── LOG.txt
    ├── .LABEL
    ├── logFile.txt
    ├── .PARAMS
    ├── READS-c0-3_bismark_bt2.bam
    └── READS-c0-3_bismark_bt2_SE_report.txt
    ```

    However getting error `Failed to read from /home/ethollem/projects/snakeFeet/output/simulated/mappedReads/MAPPED-c0-3/READS-c0-3.fastq_bismark_bt2_SE_report.txt:`. This file does in fact *not* exist.
    However there is a very similarly named file `READS-c0-3_bismark_bt2_SE_report.txt` only
    differing by the absence of the `.fastq` file extension. Is this getting left
    on the path for some reason?
