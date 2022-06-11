# Python script to generate simulated bisulfite reads for pipeline testing
# Dependent on mapping back to a genome
# It may be best to generate a genome with "chromosomes" that have specific
# properties and then generate reads from each chromosome

import numpy as np
from Bio import SeqIO


class chromosomeGenerator():
    
    def __init__(self, chromosome_id, nickname, length, c_content, c_spacing):
        self.chromosome_id = chromosome_id
        self.nickname = nickname
        self.length = length
        self.c_content = c_content
        self.c_spacing = c_spacing
        self.seq = ['N'] * self.length
    
    @property
    def spacing_method(self):
        '''Run the spacing method coressponding to `c_spacing` attribute.

        Raises:
            TypeError: C spacing string not assigned to a method.

        Returns:
            None: Executes the correct spacing method modifying `seq` attribute.
        '''
        if self.c_spacing == 'uniform':
            return self._random_c
        elif self.c_spacing == 'sin':
            return self._sinusoidal_c
        elif self.c_spacing == 'even':
            return self._even_c
        else:
            raise TypeError
    
    @property
    def total_c(self):
        '''Calculate the total C bases that should be in the final sequence
        as an int.

        Returns:
            int: Number of C bases.
        '''
        return int(self.length * self.c_content)
    
    
    def generate_sequence(self):
        '''Generate final sequence for this chromosome, store in `seq` attribute
        '''
        # Place C bases according to specified spacing method
        self.spacing_method()
        assert 'C' in self.seq
        self._fill_non_c_bases()
        assert 'N' not in self.seq

    
    def _even_c(self):
        '''Distribute C bases evenly throughout the length of the chromosome
        with approx. same distance between each C base.
        '''
        for i in range(0, self.length, int(self.length / self.total_c)):
            self.seq[i] = 'C'
    
    
    def _uniform_c(self):
        '''Distribute C bases based on random uniform distribution throughout
        the length of the sequence.
        '''
        for i in np.random.choice(range(self.length), size=self.total_c):
            self.seq[i] = 'C'
    
    
    def _sinusoidal_c(self):
        '''Use sin function to create weighted probability distribution for
        C distribution. This should result in a "wavy" distribution of Cs 
        throughout the sequence with higher probability of encountering Cs at
        peaks and lower at troughs. Period is currently fixed at 2pi/(length/20)
        '''
        
        # use sin function to generator "wavy" probability distribution
        # over the length of the sequence
        sin_func = lambda x: np.sin(x / int(self.length/20))
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
        '''After Cs have been placed add filler bases to remaining open positions
        in the sequence.
        '''
        for i, base in enumerate(self.seq):
            if base != 'C':
                base = np.random.choice(['A', 'T', 'G'])
                self.seq[i] = base


class readGenerator():
    
    def __init__(self, sequence, )
                
