'''Fragment a fasta reference.

This script takes a reference fasta file (multifasta allowed) and fragments
it with a sliding window.

Usage:
  fragmentfa.py <template> --wsize=<nt> --step=<nt> <outfile>
  fragmentfa.py (-h | --help)
  fragmentfa.py --version

Options:
  -h --help         Show this screen.
  --version         Show version.
  -w --wsize=<nt>   Size of the sliding window in nt [default: 100].
  -s --step=<nt>    Step size in nt, affecting window overlap [default: 50].
'''

from docopt import docopt
from skbio import read
import sys
sys.path.append("/Users/pi/repositories")
from toolshed.utils import window


arguments = docopt(__doc__, version='fragmentfa 0.1')
# print(arguments)
fp = arguments['<template>']
fpout = arguments['<outfile>']
wsize = int(arguments['--wsize'])
step = int(arguments['--step'])


fa = read(fp, format='fasta')


with open(fpout, 'w+') as out:
    counter = 0
    for i in fa:
        gen = window(str(i), wsize, step)
        counter = 0
        for w in gen:
            counter += 1
            out.write(
                '>{}_{}\n{}\n'.format(
                    i.metadata['id'], counter, w
                )
            )
