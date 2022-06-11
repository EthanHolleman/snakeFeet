# Python script to generate simulated bisulfite reads for pipeline testing
# Dependent on mapping back to a genome
# It may be best to generate a genome with "chromosomes" that have specific
# properties and then generate reads from each chromosome

import numpy as np


class ChromosomeGenerator():
    
    def __init__(self, chromosome_id, nickname, length, c_content):
        self.chromsome_id = chromsome_id
        self.nickname = nickname
        self.length = length
        self.c_content = c_content
        self.seq = 'N' * self.length
    
    @property
    def total_c(self):
        return int(self.length * self.c_content)
    
    def generate_sequence(self):
        pass
    
    def _uniform_c(self):
        for i in range(0, self.length, int(self.length / self.total_c)):
            self.seq[i] = 'C'
    
    
    def _random_c(self):
        for i in np.random.choice(range(self.length), size=self.total_c):
            self.seq[i] = 'C'
    
    
    def _sinusoidal_c(self):
        
        # use sin function to generator "wavy" probability distribution
        # over the length of the sequence 
        sin = np.abs(np.sin(range(self.length)))
        sin_probs = sin / sum(sin)
        
        # Select indexes to make C based on above distribution
        c_positions = np.random.choice(
            range(self.length), size=self.total_c, p=sin_probs
            )
        
        # assign C char to each position selected
        for each_pos in c_positions:
            self.seq[each_pos] = 'C'
        
    
    def _fill_non_c_bases(self):
        for i, base in enumerate(self.seq):
            if base != 'C':
                base = np.random.choice(['A', 'T', 'G'])
                self.seq[i] = base
    
                
        