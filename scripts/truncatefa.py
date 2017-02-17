''' Generate a fasta file containing reads with random bases.

This script takes a fasta as template and returns a fasta with the same
length distribution of random sequences. E.g. pass a reference, and it returns
a "random reference" of equal length. Pass a fasta containing reads, and it
returns a fasta file of random reads with the same length distribution as the
input.

Usage:
  truncatefa.py <template> --start=<start> --end=<end> <outfile>
  truncatefa.py (-h | --help)
  truncatefa.py --version

Options:
  --start=<start>
   --end=<end>
  -h --help     Show this screen.
  --version     Show version.
'''

from docopt import docopt
import progressbar
from skbio import read


arguments = docopt(__doc__, version='randomfa 0.1')
# print(arguments)
fp = arguments['<template>']
fpout = arguments['<outfile>']
start = int(arguments['--start'])
end = int(arguments['--end'])

fa = read(fp, format='fasta')


print('# of reads processed:')
with open(fpout, 'w+') as out:
    bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength)
    counter = 0
    for i in fa:
        r = str(i)[start:end]
        out.write(
            '>{}\n{}\n'.format(
                i.metadata['id'], r
            )
        )
        counter += 1
        bar.update(counter)
