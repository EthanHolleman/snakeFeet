
rule generate_reads:
    output:
        recordTable='output/simulated/substrates/recordTable.tsv',
        readDir=directory('output/simulated/substrates/reads'),
        chrDir=directory('output/simulated/substrates/chrs'),
    params:
        chrConfig=config['chrConfig']
    shell:'''
    python workflow/scripts/simulateReads.py {params.chrConfig} {output.chrDir} \
    {output.readDir} {output.recordTable}
    '''



