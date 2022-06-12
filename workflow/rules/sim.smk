from pathlib import Path


checkpoint generate_reads:
    output:
        recordTable='output/simulated/substrates/recordTable.tsv',
        readDir=directory('output/simulated/substrates/reads'),
        chrDir=directory('output/simulated/substrates/chrs'),
        bedDir=directory('output/simulated/substrates/bed')
    params:
        chrConfig=config['chrConfig']
    shell:'''
    python workflow/scripts/simulateReads.py {params.chrConfig} {output.chrDir} \
    {output.readDir} {output.recordTable} {output.bedDir}
    '''



def determine_map_random_reads_input(wildcards):

    checkpoint_output = checkpoints.generate_reads.get(**wildcards).output

    return {
        'fastq': f'{checkpoint_output[1]}/READS-{{chr_name}}.fastq',
        'genome': f'{checkpoint_output[2]}/CHR-{{chr_name}}.fa',
        'gene_index': f'{checkpoint_output[3]}/BED-{{chr_name}}.bed'
    }

    
rule map_reads_random:
    conda:
        '../envs/footloop.yml'
    input:
        fastq=lambda wildcards: determine_map_random_reads_input(wildcards)['fastq'],
        genome=lambda wildcards: determine_map_random_reads_input(wildcards)['genome'],
        gene_index=lambda wildcards: determine_map_random_reads_input(wildcards)['gene_index']
    output:
        mapped_reads_dir=directory('output/simulated/mappedReads/MAPPED-{chr_name}')
    params:
        label='PCB123'
    shell:'''
    mkdir -p output/simulated/mappedReads
    perl workflow/submodules/footLoop/footLoop.pl -r {input.fastq} -n {output.mapped_reads_dir} \
    -l {params.label} -g {input.genome} -i {input.gene_index} -Z
    '''

