import re


def parse_iav(isolate):
    '''
    parse the data from influenza name into dict

    test:
    a = 'A/mallard/Interior Alaska/6MP0155/2006(H3N8)'
    b = 'A/blue-winged Teal/Minnesota/AI09-2977/2009(H4N8)'
    c = 'A/Peru/PER175/2012(H3N2)'
    '''

    # regexp structure check

    feat = isolate.split('/')
    assert feat[0] == 'A', 'Not Influenza A Virus.'

    subtype = re.search(r'\((.*?)\)', isolate).group(1)
    feat[-1] = feat[-1].split('(')[0]
    if len(feat) == 4:
        host = 'human'
        geo = feat[1]
    else:
        host = feat[1].lower()
        geo = feat[2]

    return({
        'influenza': feat[0],
        'host': host,
        'subtype': subtype,
        'geolocation': geo
        })


def parse_date(date):
    '''
    Parse (influenza) dates (source: NCBI Genomes, i.e. GenBank) into
    nicely searchable format for insertion in zoo database. Four formats
    are recognized:

    - 1976
    - 2011/01
    - 2011/01/27  # ymd
    - ('NON', 'Unknown', '')

    Usage:

    parse_date('2019/08')
    # {'d': '', 'm': 8, 'y': 2019}
    '''
    record = {'y': '', 'm': '', 'd': ''}
    if date in ('NON', 'Unknown', 'unknown', ''):
        return record
    else:
        s = date.split('/')
        for i in zip(range(3), 'y m d'.split(' ')):
            j, tag = i
            try:
                record[tag] = int(s[j])
            except IndexError:
                continue
        return record
