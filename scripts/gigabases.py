'''
Count number of bases in fastq
'''

# venv-bio
from Bio import SeqIO
import click
from tqdm import tqdm


@click.command()
@click.option('-i', help='File path to fastq.')
def gigabases(i):
    fq = SeqIO.parse(i, format='fastq')
    n = 0
    for i in tqdm(fq):
        n += len(i)
    print('Number of gigabases:', round(n / 1e9, 3))
    # this is about file size / 2


if __name__ == '__main__':
    gigabases()