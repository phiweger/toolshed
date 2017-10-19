# TODO: write tests

from Bio.Seq import Seq
import itertools
import numpy as np
import random
import re
from scipy.stats import uniform


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


def kmerize(seq, ksize, canonical=False):
    '''
    returns a generator and yields all (canonical) kmers of length ksize from
    sequence seq

    canonical .. only the lexicographically smaller of a kmer and its
    reverse complement is returned; important when implementing minhash
    of k-mers
    '''
    from Bio.Seq import Seq

    for i in range(len(seq) - ksize + 1):
        kmer = seq[i:i+ksize]

        if not canonical:
            yield kmer
        else:
            # TODO: speed this up later by circumventing Biopython
            rc = Seq(kmer).reverse_complement().__str__()
            if kmer < rc:
                yield kmer
            else:
                yield rc


def mutate(text, error_rate, alphabet=None):
    '''
    insert changes in a text, i.e. mistakes, increasing the
    distance to the original

    alphabet=ascii_letters
    alphabet=set(text)

    don't modify alphabet, i.e. transforming the string to lower
    '''
    if alphabet is None:
        # use text'alphabet by default
        alphabet = list(set(text))
    lt = len(text)
    num_mutations = sum(uniform.rvs(loc=0, scale=1, size=lt) < error_rate)
    sample = random.sample(range(0, lt), num_mutations)
    l = list(text)
    for i in sample:
        l[i] = random.choice(alphabet)
    return(''.join(l))


def fragment(seq, fsize):
    '''
    Fragment seq into fragments of length <fsize>.

    Return generator.
    '''
    for f in np.arange(0, len(seq) - fsize + 1, fsize):
        yield(seq[f:f+fsize])


def hamming(ref, seq, relative=True):
    '''
    in: 2 strings (or iterables) of equal length, if unequal, the larger one
    is truncated
    - ref .. reference (with gaps)
    - seq .. red
    distinction ref, seq does not matter really

    out: (relative) Hamming distance
    '''
    num_mismatch = 0
    for i in zip(ref, seq):
        a, b = i
        if a != b:
            num_mismatch += 1
        # the same can be done like so (left here for testing):
        # if len(set(i)) == 2:  # i.e. mismatch
        #     num_mismatch += 1
    if relative:
        return(num_mismatch / len(ref))  # [^1]
    else:
        return(num_mismatch)


def test_hamming():
    a = 'abc'
    b = 'aba'
    assert hamming(a, b, relative=False) == 1


def stream(seq):
    '''
    in: a string

    out: a generator which yields one letter at a time
    '''
    for i in seq:
        yield(i)


def random_seq(
        length,
        alphabet=('A', 'C', 'T', 'G'),
        prob=(0.25, 0.25, 0.25, 0.25)):
    '''
    stackoverflow, 30205962

    random_seq(10)
    # 'GTATGCGACC'
    '''
    return ''.join(np.random.choice(alphabet, p=prob) for _ in range(length))


def chunks(l, n):
    '''
    Yield successive n-sized chunks from l (stackoverflow, 312443).

    a = [1, 2, 3, 4]
    list(chunks(a, 2))
    # [[1, 2], [3, 4]]

    Returns empty list if list empty.

    For overlapping chunks, see windows()
    '''
    for i in range(0, len(l), n):
        yield l[i:i + n]


def windows(iterable, length=2, overlap=0):
    '''
    Returns a generator of windows of <length> and with an <overlap>.

    Shamelessly stolen from: Python cookbook 2nd edition, chapter 19
    '''
    it = iter(iterable)
    results = list(itertools.islice(it, length))
    while len(results) == length:
        yield results
        results = results[length-overlap:]
        results.extend(itertools.islice(it, length-overlap))
    if results:
        yield results


# def window(seq, wsize, step):
#     '''
#     Sliding window of <wsize> moving by <step> nt along <seq>.
#     '''
#     for i in np.arange(0, len(seq) - wsize + 1, step):
#         w = seq[i:i+wsize]
#         yield w


def bottomk_sampling_rate(seq, ksize=15, n=100):
    '''
    rate = sketch size / number k-mers (unique, canonical)

    Sample e.g. bottom 3 percent of possible k-mers:

    bottomk_sampling_rate(seq, n=25, ksize=15)
    # 0.03
    '''
    return n / len(set(kmerize(seq, ksize=ksize, canonical=True)))



'''
[^1]: T. Laver et al., “Assessing the performance of the Oxford Nanopore
Technologies MinION,” Biomolecular Detection and Quantification, vol. 3, pp.
1–8, Mar. 2015.
'''
