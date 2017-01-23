'''Mix read sets.

Given a json fomatted file of file paths to fasta files with associated weight,
this script creates a fasta file with the specified read proportions. Note
that this creates a bias if the read length distribution of the samples is
different. I.e. while the read count of sample X might be 10 % of the total
number of reads in the output, it might not have 10 % of the nucleotides if
its average read length is shorter than another sample's.

File paths are specified in json format:

{
    human: 0.9,
    virus: 0.1
}

It is possible to truncate the samples' read distribution for speedup.

Usage:
  readmix.py <json> [--total=<reads>] [--longest=<nt>] <outfile>
  readmix.py (-h | --help)
  readmix.py --version

Options:
  -h --help             Show this screen.
  -t --total=<reads>    Total number of reads [default: 1m].
  -l --longest=<nt>     Speed in knots [default: 100k].
'''

from docopt import docopt
import json
from pyfaidx import Fasta
import random
import re


def convert_abbrev_int(num):
    '''
    accepts 1k for thousand and 1m for million
    implementation idea: stackoverflow, 430079
    note that only integers are allowed
    if abbreviated, returns int(expansion)
    if input not abbreviated, returns int(input)
    '''
    d = {'k': 1000, 'm': 1000000}

    match = re.match(r'([0-9]+)([mk])', num, re.I)  # re.I .. case ignore
    if match:
        items = match.groups()
    try:
        return int(items[0]) * d[items[1]]
    except UnboundLocalError:  # input not abbreviated
        return int(num)


class Sample():  # in python 3 no need to inherit from "object"
    def __init__(self, fp, weight):
        self.fp = fp
        self.weight = weight
        self.share = None
        self.file = None

    def __str__(self):
        return('fp: {}, weight: {}'.format(self.fp, self.weight))

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(self.fp)

    def __eq__(self, other):
        return self.fp == other.fp

    def read(self):
        self.file = Fasta(self.fp)

    def calc_share(self, total):  # TODO: base={alphabet, read}
        self.share = int(self.weight * total)


arguments = docopt(__doc__, version='readmix 0.1')
# print(arguments)

fpout = arguments['<outfile>']
total = convert_abbrev_int(arguments['--total'])
longest = convert_abbrev_int(arguments['--longest'])
with open(arguments['<json>'], 'r+') as file:
    d = json.load(file)


try:
    assert sum(d.values()) == 1
except AssertionError:
    print('Weights do not add up to 1.')
    exit()


counter = 0
with open(fpout, 'w+') as out:
    for fp, weight in d.items():
        s = Sample(fp, weight)
        s.calc_share(total)
        s.read()

        counter = 0
        while counter < s.share:
            name = random.sample(s.file.keys(), 1)[0]
            seq = s.file[name]
            if len(seq) <= longest:
                out.write(
                    '>{}\n{}\n'.format(name, seq)
                    )
                counter += 1
                if counter % 10 == 0:
                    print(counter)
