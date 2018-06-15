# This file converts incoming words into mini-sdrs by registering features of a word
# The input to this file are a bunch of lists
# From these lists we create regex that identify a feature's 
import re

def load_category_from_file(fpath):
    """Take a one word per line file and return a regex for the concatenation '^(w1|w2)$'"""
    with open(fpath, 'r') as source:
        ways = [line.strip().lower() for line in source]
    return r'^(' + "|".join(ways) + r')$'

def load_category_from_file_no_bookends(fpath):
    """Take a one word per line file and return a regex for the concatenation '(w1|w2)', NOTE the missine ^ and $"""
    with open(fpath, 'r') as source:
        ways = [line.strip().lower() for line in source]
    return r'(' + "|".join(ways) + r')'

negatives = load_category_from_file('data/words_non_address.csv')
ways = load_category_from_file('data/words_way.csv')
common_street = load_category_from_file('data/words_common_street.csv')
structures = load_category_from_file('data/words_structures.csv')
preps = load_category_from_file('data/words_preps.csv')
conjs = load_category_from_file('data/words_conjs.csv')
apts = load_category_from_file('data/words_apts.csv')
nths = load_category_from_file('nth.csv')
dirs = load_category_from_file('dirs.csv')
arti = load_category_from_file('data/words_arti.csv')
pre  = load_category_from_file('pre.csv')
deleg = load_category_from_file('deleg.csv')
wordways = load_category_from_file('data/words_word_way.csv')
gfeatures = load_category_from_file('data/words_gfeatures.csv')
sp_arti = load_category_from_file('data/words_sp_arti.csv')
sp_way = load_category_from_file('data/words_sp_way.csv')
sp_pre = load_category_from_file('data/words_sp_pre.csv')
word_numbers = load_category_from_file('data/words_numbers.csv')
apts_base = load_category_from_file_no_bookends('data/words_apts.csv')
# http://maf.directory/zp4/abbrev.html

def encoder(word, trim=True):
    rex_gigit_direction = r'^\d+(n|s|e|w|sw|se|nw|ne)$'
    rex_digdashal = r'^\d+-[a-z]+$'
    rex_alnum = r'^(\d+[a-z]+|[a-z]+\d+)[\da-z]*$'
    rex_alnumdashnum = r'^[a-z]\d+-\d+$'
    rex_oneal_digits = r'^[a-z]\d+'
    encodings = [
        # LETTERS ONLY
        ('ALPHA',           [r'^[a-z\'A-Z]+$']),
            ('LETTER',      [r'^[a-zA-Z]$']),
            ('POST',        [r'^p$', r'^post$' ]),
            ('OFFICE',      [r'^o$', r'^office$' ]),
            ('TH',          [r'^th$' ]),
            ('WAY',         [ ways]),
            ('WORDWAY',     [ wordways ]),
            ('COMMONST',    [ common_street ]),
            ('GFEATURE',    [ gfeatures ]),
            ('STRUCTURE',    [ structures ]),
            ('APT',         [ apts ]),
            ('ARTI',        [ arti ]),
            ('PREP',        [ preps ]),
            ('CONJ',        [ conjs ]),
            ('WAYCOKY',      [ r'^county$', r'^co$', r'^ky$', r'^state$', r'^us$' ]), # county and co show up in '123 CO RD 456'
            ('SP_ARTI',     [ sp_arti ]),
            ('SP_WAY',      [ sp_way ]),
            ('SP_PRE',      [ sp_pre ]),
            ('FARM2MARK',   [ r'^fm$' ]),
            ('PRE',         [ pre ]),
            ('DIR',         [ dirs ]),
            ('POB2',        [ r'^box$', r'^bxo$' ]),
            ('POBHC',       [ r'^(hc|rr)$' ]),
            ('POBOX1',       [ r'^pobox$' ]),
            ('DRAWER',       [ r'^drawer$' ]),
            ('DELEG',       [ r'^attn$', r'^attn:$', r'^c\/o$', r'^co$' ]),
            ('POB0',        [ r'^po$', r'^p\.o\.$' ]),
            ('NEGATIVE',        [ negatives ]),
        # NUMBERS ONLY
        ('DIGIT',           [r'^\d+$']),
        ('DIGDASH',         [ r'\d+-\d+$' ]),
        ('DIGSLASH',        [ r'\d+/\d+$' ]),
        ('DASH',            [ r'^-$' ]),

        # MIXED LETTERS AND NUMBERS
        ('ADR_HEAD',        [r'^\d+$', word_numbers, r'^[nsew]\d+$', r'^#\d+$', r'\d+-\d+$', r'^[nsew]\d+[nsew]\d+$',
                                rex_gigit_direction,
                                rex_digdashal,
                                rex_oneal_digits,
                                #rex_alnum
                                ]),
        ('ALNUM',           [rex_alnum]),
            ('DIGDASHAL',   [r'^\d+-[a-z]+$'] ),
            ('BOXNUM',      [r'^box\d+$']),
            ('ALDASHDIG',   [r'^[a-z]+-\d+$'] ),
            ('NUMSTR',      [r'^\d+[a-z]+$' ]),
                ('NTH',     [ nths, r'^[nsew]\d+(rd|st|th)' ]),
                ('NUMS_1AL',[ r'^\d+[a-z]$' ]),
                ('APT_NUM', [r'^' + apts_base + r'\d+$', r'^' + apts_base + r'[a-z]$', rex_alnumdashnum ]),
                ('DIG-DIGTH', [ r'^\d+-\d+(th|st|rd)$' ]),
                ('DIG-AL6',  [ r'^\d+[a-z]{6,}$' ]),
        # SYMBOLS ONLY
        ('COMMA',           [r'^,$']),
        ('PERIOD',          [r'^\.$']),
        ('POUND',           [r'^#$']),
        ('AND',             [r'^&$', r'^and$' ]),

        # LETTERS AND SYMBOLS
        ('WORDDASHWORD',    [ r'^[a-z]+-[a-z]+$' ]),

        # NUMBERS AND SYMBOLS
        ('POUNDDIG',           [r'^#\d+$']),

        # INTERNAL MARKERS
        ('ADDRESS', [r'^:adr$']),
        ('ATTN', [r'^:deleg$']),
        ('POBOX', [r'^:box$']),
    ]
    encoding = [key for key, rexs in encodings for rex in rexs if re.match(rex, word)]
    if not trim:
        return encoding
    else:
        if any([key in ['P','O','NEGATIVE', 'TH','SP_ARTI','LETTER', 'WORDWAY', 'WAY', 'APT', 'ARTI', 'PRE', 'DIR', 'DELEG', 'POB2', 'POB0', 'POBOX1', 'FARM2MARK'] for key in encoding]) and 'ALPHA' in encoding:
            encoding.remove('ALPHA')  # Redudant category level if we have probable meaning
        if any([key in ['NUMS_1AL', 'NUMSTR', 'NTH'] for key in encoding]) and 'ALNUM' in encoding:
            encoding.remove('ALNUM')  # Redudant category level if we have probable meaning
        if any([key in ['NUMS_1AL', 'NTH'] for key in encoding]) and 'NUMSTR' in encoding:
            encoding.remove('NUMSTR')

        return encoding
