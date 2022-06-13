

# rule call_peaks:
#     conda:
#         '../envs/footloop.yml'
#     input:
#         mapped_reads_dir=''
#     output:
#         called_peaks_dir=directory('')
#     shell:'''
#     submodules/footPeak.pl -n {input.mapped_reads_dir} -o {output.called_peaks_dir}
#     '''
    