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
        'fastq': f'{checkpoint_output[1]}/READS_{{chr_name}}.fq',
        'genome': f'{checkpoint_output[2]}/CHR_{{chr_name}}.fa',
        'gene_index': f'{checkpoint_output[3]}/BED_{{chr_name}}.bed'
    }


rule gzip_random_fastq:
    input:
        fastq=lambda wildcards: determine_map_random_reads_input(wildcards)['fastq']
    output:
        'output/simulated/substrates/gzipReads/READS_{chr_name}.fq.gz'
    shell:'''
    gzip -c {input.fastq} > {output}
    '''

    
rule map_reads_random:
    conda:
        '../envs/footloop.yml'
    input:
        fastq='output/simulated/substrates/gzipReads/READS_{chr_name}.fq.gz',
        genome=lambda wildcards: determine_map_random_reads_input(wildcards)['genome'],
        gene_index=lambda wildcards: determine_map_random_reads_input(wildcards)['gene_index']
    output:
        mapped_reads_dir=directory('output/simulated/mappedReads/MAPPED_{chr_name}')
    params:
        label='PCB123'
    shell:'''
    mkdir -p {output}
    perl workflow/submodules/footLoop/footLoop.pl -r {input.fastq} -n {output.mapped_reads_dir} \
    -l {params.label} -g {input.genome} -i {input.gene_index} -Z -L 100
    '''

# Additional parameters for call peaks
# ====================================
# -d minDis  : 250
# -s grpSize : 200
# -k Dist    : 50
# -t thrshld : 55
# -w window  : 20

rule call_peaks:
    conda:
        '../envs/footloop.yml'
    input:
        mapped_reads_dir='output/simulated/mappedReads/MAPPED_{chr_name}'
    output:
        called_peaks=directory('output/simulated/calledPeaks/PEAKS_{chr_name}')
    params:
        min_peak_length=100,  # default = 100
        conversion_thres=0.55,  # default = 0.55
    shell:'''
    mkdir -p {output}
    perl workflow/submodules/footLoop/footPeak.pl -n {input.mapped_reads_dir} \
    -l {params.min_peak_length} -o {output.called_peaks}
    '''

