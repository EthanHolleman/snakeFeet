

rule map_reads_random:
    conda:
        '../envs/footloop.yml'
    input:
        fastq='output/simulated/substrates/reads/READS-{chr_name}.fastq',
        genome='output/simulated/substrates/chrs/CHR-{chr_name}.fa'
    output:
        mapped_reads_dir=directory('output/simulated/mappedReads/MAPPED-{chr_name}')
    params:
        label='PCB123'
    shell:'''
    mkdir -p output/simulated/mappedReads
    perl workflow/submodules/footLoop/footLoop.pl -r {input.fastq} -n {output.mapped_reads_dir} \
    -l {params.label} -g {input.genome} -Z
    '''

rule call_peaks:
    conda:
        '../envs/footloop.yml'
    input:
        mapped_reads_dir=''
    output:
        called_peaks_dir=directory('')
    shell:'''
    submodules/footPeak.pl -n {input.mapped_reads_dir} -o {output.called_peaks_dir}
    '''
    