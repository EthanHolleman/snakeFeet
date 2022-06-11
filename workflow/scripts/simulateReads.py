# Python script to generate simulated bisulfite reads for pipeline testing
# Dependent on mapping back to a genome
# It may be best to generate a genome with "chromosomes" that have specific
# properties and then generate reads from each chromosome

import numpy as np
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
import pandas as pd
from pathlib import Path
import argparse


class chromosomeGenerator:
    def __init__(self, chromosome_id, nickname, length, c_content, c_spacing):
        self.chromosome_id = chromosome_id
        self.nickname = nickname
        self.length = length
        self.c_content = c_content
        self.c_spacing = c_spacing
        self.seq = ["N"] * self.length
        self.sub_id = 0

    @property
    def spacing_method(self):
        """Run the spacing method coressponding to `c_spacing` attribute.

        Raises:
            TypeError: C spacing string not assigned to a method.

        Returns:
            None: Executes the correct spacing method modifying `seq` attribute.
        """
        if self.c_spacing == "uniform":
            return self._random_c
        elif self.c_spacing == "sin":
            return self._sinusoidal_c
        elif self.c_spacing == "even":
            return self._even_c
        else:
            raise TypeError

    @property
    def total_c(self):
        """Calculate the total C bases that should be in the final sequence
        as an int.

        Returns:
            int: Number of C bases.
        """
        return int(self.length * self.c_content)

    def get_sequence(self):
        """Generate final sequence for this chromosome, store in `seq` attribute
        """
        # Check if previous sequence has already been generated. If True
        # then delete it
        if "C" in self.seq:
            self.seq = ["N"] * self.length

        self.spacing_method()
        assert "C" in self.seq
        self._fill_non_c_bases()
        assert "N" not in self.seq
        self.sub_id += 1

    def __next__(self):
        self.get_sequence()
        return self._to_seq_record()

    def _even_c(self):
        """Distribute C bases evenly throughout the length of the chromosome
        with approx. same distance between each C base.
        """
        for i in range(0, self.length, int(self.length / self.total_c)):
            self.seq[i] = "C"

    def _uniform_c(self):
        """Distribute C bases based on random uniform distribution throughout
        the length of the sequence.
        """
        for i in np.random.choice(range(self.length), size=self.total_c):
            self.seq[i] = "C"

    def _sinusoidal_c(self):
        """Use sin function to create weighted probability distribution for
        C distribution. This should result in a "wavy" distribution of Cs 
        throughout the sequence with higher probability of encountering Cs at
        peaks and lower at troughs. Period is currently fixed at 2pi/(length/20)
        """

        # use sin function to generator "wavy" probability distribution
        # over the length of the sequence
        sin_func = lambda x: np.sin(x / int(self.length / 20))
        sin = np.abs(np.sin(range(self.length)))
        sin_probs = sin / sum(sin)

        # Select indexes to make C based on above distribution
        c_positions = np.random.choice(
            range(self.length), size=self.total_c, p=sin_probs
        )

        # assign C char to each position selected
        for each_pos in c_positions:
            self.seq[each_pos] = "C"

    def _fill_non_c_bases(self):
        """After Cs have been placed add filler bases to remaining open positions
        in the sequence.
        """
        for i, base in enumerate(self.seq):
            if base != "C":
                base = np.random.choice(["A", "T", "G"])
                self.seq[i] = base

    def _to_seq_record(self):
        record = SeqRecord(
            Seq("".join(self.seq)),
            id=f"c{self.chromosome_id}-{self.sub_id}",
            name=self.nickname,
            description="Random chromosome C content:{self.c_content} with {self.c_spacing} distribution",
        )
        return record



class readGenerator:
    def __init__(
        self, seq_record, conversion_eff, avg_loop_length=200, loop_length_sd=20
    ):
        self.seq_record = seq_record
        self.conversion_eff = conversion_eff
        self.read_length = read_length
        self.avg_loop_length = avg_loop_length
        self.read_counter = 0
        self.conversion_track = []  # 2=Converted C  # 1=Unconverted C # 0=Non-C base

    def get_read(self):
        '''Generate a single read based on class attributes.

        Returns:
            SeqRecord: BioPython SeqRecord object.
        '''
        length = np.random.normal(loc=avg_loop_length, scale=loop_length_sd)
        start_pos = np.random.randint(0, len(seq_record.seq) - length)
        read_bases = self.seq_record.seq[start_pos : start_pos + length]
        converted_read = ["N"] * len(read_bases)

        for each_base in read_bases:
            if "C" == each_base:
                if np.random.random_sample <= conversion_eff:
                    converted_read.append("T")  # C->T conversion occurs
                    self.conversion_track.append("2")
                    continue
                else:
                    self.conversion_track.append("1")
                    continue
            converted_read.append(each_base)
            self.conversion_track.append("0")

        self.read_counter += 1

        return SeqRecord(
            Seq("".join(converted_read)),
            id=f"{seq_record.id}+r{self.read_counter}",
            name=f"{seq_record.name} read {self.read_counter}",
            annotations={
                "conversion_eff": self.conversion_eff,
                "read_length": length,
                "read_id": self.read_counter,
                "read_start": self.start_pos,
                "avg_loop_length": self.average_loop_length,
                "chr_description": self.seq_record.description,
                "chr_id": self.seq_record.id,
                "chr_name": self.seq_record.name,
                "read_seq": "".join(converted_read),
                "conversion_track": "".join(self.conversion_track),
            },
            letter_annotations={"solexa_quality": [40] * length},
        )

    def __next__(self):
        return self.get_read()


def make_chr_and_reads(chromosome_table, chr_output_dir, read_output_dir, record_path):
    read_records = []
    for index, row in chromosome_table:
        # Prepare generator to make chromosomes with characteristics specified
        # by current row of chromosome table
        generator = chromosomeGenerator(
            row["chromosome_id"],
            row["nickname"],
            row["length"],
            row["c_content"],
            row["c_spacing"],
        )
        for i in row["num_copies"]:
            current_chrom = next(generator)
            fasta_name = f"CHR-{current_chrom.id}.fa"
            fasta_path = Path(chr_output_dir).joinpath(fasta_name)
            # write generated chromosome to fasta file
            with open(str(fasta_path), "w") as handle:
                SeqIO.write([current_chrom], handle, "fasta")

            # generate reads from chromosome
            read_gen = readGenerator(current_chrom, row["conversion_eff"])
            reads = [next(read_gen) for _ in row["num_reads"]]

            # Set location for writing reads to
            fastq_name = f"READS-{current_chrom.id}.fastq"
            fastq_path = Path(read_output_dir).joinpath(fastq_name)

            # record read information in table for later reference by other
            # programs and easier data wrangling when plotting
            for read in reads:
                read.annotations["fastq_path"] = str(fastq_path)
                read.annotations["chr_fasta_path"] = str(fasta_path)
                read_records.append(read.annotations)

            # write reads to fastq file
            with open(str(fastq_path), "w") as handle:
                SeqIO.write(reads, handle, "fastq")

    # At this point all reads and chromosomes should have been written
    # and recorded in read_records, now just need to save read_records as
    # a tsv file for later use.

    pd.DataFrame(read_records).to_csv(record_path, index=False, sep="\t")

    return record_path


def get_args():
    
    parser = argparse.ArgumentParser(description='Generate random bisulfite reads')
    parser.add_argument(
        'chrTable', metavar='C', help='Path to chromosome configuration table')
    parser.add_argument(
        'chrOut', metavar='F', 
        help='Path to directory to write chromosome fasta files to. Reads are \
            generated from these "chromosomes".'
    )
    parser.add_argument(
        'readOut', metavar='R',
        help='Path to directory to write bisulfite converted reads to. 1 fastq \
            file is generated per chromosome containing all reads for that \
            particular chromosome.'
    )
    parser.add_argument(
        'recordOut', metavar='R',
        help='Path to write record table to. This is a tsv file containing \
            descriptions of all reads generated.'
    )
    return parser.parse_args()
    


def main():

    args = get_args()
    
    chromosome_table = pd.read(args.chrTable)
    make_chr_and_reads(chromosome_table, args.chrOut, args.readOut, args.recordOut)


if __name__ == '__main__':
    main()
    
    
   
