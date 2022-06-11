

rule map_reads:
    conda:
        '../envs/footloop.yml'
    input:
        fastq='',
        index='',
        genome=''
    output:
        mapped_reads_dir=directory('')
    params:
        label=''
    shell:'''
    submodules/footLoop.pl -r {input.fastq} -n {output.mapped_reads_dir} \
    -l {params.label} -i {input.index} -g {input.genome}
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
    