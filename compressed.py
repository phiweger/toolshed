# https://github.com/dib-lab/sourmash/blob/f76938edf1125c7aee61b9039dcf30add5b215f8/sourmash_lib/signature.py


mport io
import gzip
import bz2file


def _guess_open(filename):
    """
    Make a best-effort guess as to how to parse the given sequence file.
    Handles '-' as shortcut for stdin.
    Deals with .gz and .bz2 as well as plain text.
    """
    magic_dict = {
        b"\x1f\x8b\x08": "gz",
        b"\x42\x5a\x68": "bz2",
    }  # Inspired by http://stackoverflow.com/a/13044946/1585509

    if filename == '-':
        filename = '/dev/stdin'

    bufferedfile = io.open(file=filename, mode='rb', buffering=8192)
    num_bytes_to_peek = max(len(x) for x in magic_dict)
    file_start = bufferedfile.peek(num_bytes_to_peek)
    compression = None
    for magic, ftype in magic_dict.items():
        if file_start.startswith(magic):
            compression = ftype
            break
    if compression is 'bz2':
        sigfile = bz2file.BZ2File(filename=bufferedfile)
    elif compression is 'gz':
        if not bufferedfile.seekable():
            bufferedfile.close()
            raise ValueError("gziped data not streamable, pipe through zcat \
                            first")
        sigfile = gzip.GzipFile(filename=filename)
    else:
        sigfile = bufferedfile

    return sigfile