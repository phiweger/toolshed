'''Generate a fasta file containing reads with random bases.

This script takes a fasta as template and returns a fasta with the same
length distribution of random sequences. E.g. pass a reference, and it returns
a "random reference" of equal length. Pass a fasta containing reads, and it
returns a fasta file of random reads with the same length distribution as the
input.

Usage:
  randomfa.py <template> <outfile>
  randomfa.py (-h | --help)
  randomfa.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.
'''

from docopt import docopt
import hashlib
import progressbar
from skbio import read
import sys
sys.path.append("/Users/pi/repositories")
from toolshed.utils import random_seq


arguments = docopt(__doc__, version='randomfa 0.1')
# print(arguments)
fp = arguments['<template>']
fpout = arguments['<outfile>']


fa = read(fp, format='fasta')


print('# of reads processed:')
with open(fpout, 'w+') as out:
    bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength)
    counter = 0
    for i in fa:
        r = random_seq(len(str(i)))
        m = hashlib.md5()
        m.update(r.encode('utf-8'))
        out.write(
            '>{}\n{}\n'.format(
                m.hexdigest(), r
            )
        )
        counter += 1
        bar.update(counter)
