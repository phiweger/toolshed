from Bio import SeqIO
import click
from tqdm import tqdm


@click.command()
@click.option('-i', help='File path to fastq.')
@click.option('-o', help='File path to output.')
def back_transcribe(i, o):
    '''
    This script transcribes RNA data (e.g. generated through direct RNA sequencing
    using nanopores).

    Example:

    python back_transcribe -i virus.rna.fq -o virus.dna.fq

    alternative in bash,
    https://twitter.com/martinalexsmith/status/920766849385562112

    awk '{ if (NR%4 == 2) {gsub(/U/,"T",$1); print $1} else print }' \
    virus.rna.fq > virus.dna.fq
    '''

    fq = SeqIO.parse(i, format='fastq')
    '''
    The typical nanopore read header looks like this:

    "7a8efdc9-e2be-48a4-a07b-8b1b64906813 runid=fcc498e784c2a606a26becb19cfb7a3fc0cbe0f2 read=1181 ch=24 start_time=2017-09-05T15:56:57Z"

    Biopython is smart and uses only the first part before the first space as UID,
    e.g. "7a8efdc9-e2be-48a4-a07b-8b1b64906813" in the example above. Compare

    - r.name
    - r.description
    '''
    print('Back-transcibing sequences:')
    with open(o, 'w+') as out:

        for r in tqdm(fq):
            r.seq = r.seq.back_transcribe()
            SeqIO.write(r, out, 'fastq')
        print('Done.')

if __name__ == '__main__':
    back_transcribe()