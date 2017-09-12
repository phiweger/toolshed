'''
Neat helper function to print something to stderr.

source:
https://github.com/dib-lab/sourmash/blob/a9e49f6b68823f17179142512784a164d5cd67cf/sourmash_lib/logging.py
'''

import sys


_quiet = False
def set_quiet(val):
    global _quiet
    _quiet = bool(val)


def print_results(s, *args, **kwargs):
    print(s.format(*args, **kwargs), file=sys.stdout)
    sys.stdout.flush()


def notify(s, *args, **kwargs):
    '''A simple logging function => stderr.

    Example:

    notify('oh, {} has {}', 'something', 'happened')
    # oh, something has happened
    '''
    if not _quiet:
        print(s.format(*args, **kwargs), file=sys.stderr,
              end=kwargs.get('end', u'\n'))
        if kwargs.get('flush'):
            sys.stderr.flush()


def error(s, *args, **kwargs):
    "A simple error logging function => stderr."
    print(s.format(*args, **kwargs), file=sys.stderr)
    if kwargs.get('flush'):
        sys.stderr.flush()

