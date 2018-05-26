import os
import re
from hydraseq import Hydraseq

print("Starting script now")

def load_category_from_file(fpath):
    """Take a one word per line file and return a regex for the concatenation '^(w1|w2)$'"""
    with open(fpath, 'r') as source:
        ways = [line.strip().lower() for line in source]
    return r'^(' + "|".join(ways) + r')$'

def w(str_sentence):
    return re.findall(r"[\w'/-:]+|[.,!?;#&]", str_sentence)

seq = Hydraseq('input')

ways = load_category_from_file('ways.csv')
apts = load_category_from_file('apts.csv')
nths = load_category_from_file('nth.csv')
dirs = load_category_from_file('dirs.csv')
arti = load_category_from_file('arti.csv')
pre  = load_category_from_file('pre.csv')
deleg = load_category_from_file('deleg.csv')
print(apts)
def encoder(word, trim=True):
    encodings = [
        # LETTERS ONLY
        ('ALPHA', [r'^[a-z]+$']), 
            ('LETTER', [r'^[a-z]$']),
            ('WAY',  [ ways ]),
            ('APT', [ apts ]),
            ('ARTI', [ arti ]),
            ('PRE',  [ pre ]),
            ('DIR',  [ dirs ]),
            ('POB2', [r'^box$']),
            ('DELEG', [r'^attn$', r'^attn:$', r'^c\/o$', r'^co$' ]),
            ('POB0', [r'^po$', r'^p\.o\.$']),
        
        # NUMBERS ONLY
        ('DIGIT', [r'^\d+$']), 
        
        # MIXED LETTERS AND NUMBERS
        ('ALNUM', [r'^(\d+[a-z]+|[a-z]+\d+)[\da-z]*$']),
            ('NUMSTR', [r'^\d+[a-z]+$' ]),
                ('NTH',    [ nths ]),
                ('NUMS_1AL', [ r'^\d+[a-z]$' ]),
            ('APT_NUM', [ r'apt\d+$', r'unit\d+$', r'bldg\d+$', r'ste\d+$', r'suite\d+$']),
        
        # SYMBOLS ONLY
        ('COMMA', [r'^,$']),
        ('PERIOD', [r'^\.$']),
        ('POUND', [r'^#$']),
        
        # LETTERS AND SYMBOLS
        
        # NUMBERS AND SYMBOLS

        # INTERNAL MARKERS
        ('ADDRESS', [r'^:adr$']),
        ('ATTN', [r'^:deleg$']),
        ('POBOX', [r'^:box$']),
    ]
    encoding = [key for key, rexs in encodings for rex in rexs if re.match(rex, word)]
    if not trim:
        return encoding
    else:
        if any([key in ['LETTER', 'WAY', 'APT', 'ARTI', 'PRE', 'DIR', 'DELEG', 'POB2', 'POB0'] for key in encoding]) and 'ALPHA' in encoding:
            encoding.remove('ALPHA')  # Redudant category level if we have probable meaning
        if any([key in ['NUMS_1AL', 'NUMSTR', 'NTH'] for key in encoding]) and 'ALNUM' in encoding:
            encoding.remove('ALNUM')  # Redudant category level if we have probable meaning
        if any([key in ['NUMS_1AL', 'NTH'] for key in encoding]) and 'NUMSTR' in encoding:
            encoding.remove('NUMSTR')

        return encoding



# THOU SHALL NOT SEQUENCE THREE ALPHAS IN A ROW!
def train_with_provided_list(seq, matrix_lst):
    """matrix list means [['DIGIT'],['ALPHA'],['WAY']] for example"""
    return seq.insert(matrix_lst, is_learning=True).get_next_values()

import csv
with open('address_tuples_edited.csv', 'r') as source:
    csv_file = csv.DictReader(source)
    for row in csv_file:
        lst_sequence = eval(row['SEQUENCE'])
        lst_sequence.append(['ADDRESS'])
        train_with_provided_list(seq, lst_sequence)

# valid po box
train_samples = [
    ("po box 1234", [['POB0'],['POB2'],['DIGIT']]),
    ("box 999",      [['POB2'],['DIGIT']]),
]
for ts, matrix_lst in train_samples:
    matrix_lst.append(['POBOX'])
    train_with_provided_list(seq, matrix_lst)

# valid attn
train_samples = [
    ("c/o john smith",     [['DELEG'],['ALPHA'],['ALPHA']]),
    ("attn john smith",    [['DELEG'],['ALPHA'],['ALPHA']]),
    ("attn: john smith",   [['DELEG'],['ALPHA'],['ALPHA']]),
    ("c/o john",           [['DELEG'],['ALPHA']]),
]
for ts, matrix_lst in train_samples:
    matrix_lst.append(['ATTN'])
    train_with_provided_list(seq, matrix_lst)

def encode_from_word_list(arr_st):
    """Expects ['123', 'main', 'st]"""
    assert isinstance(arr_st, list)
    if arr_st: assert isinstance(arr_st[0], str)
    return [encoder(word) for word in arr_st]

def is_address(seq, arr_st):
    """Expects ["123","main","st"]"""
    return any([pred == 'ADDRESS' for pred in seq.look_ahead(encode_from_word_list(arr_st)).get_next_values()])

def is_pobox(seq, arr_st):
    """Expects ["123","main","st"]"""
    assert isinstance(arr_st, list)
    return any([pred == 'POBOX' for pred in seq.look_ahead(encode_from_word_list(arr_st)).get_next_values()])


def is_deleg(seq, arr_st):
    """Expects ["123","main","st"]"""
    assert isinstance(arr_st, list)
    return any([pred == 'ATTN' for pred in seq.look_ahead(encode_from_word_list(arr_st)).get_next_values()])


def get_markers(seq, sent, lst_targets):
    """Input is like '123 main str' and returns a list of lists
        RETURNS: a list of list, each list being a candidate and having these values.
            idx_beg, idx_end, length, matches (ADDRESS etc), sequence
        ATTN!!  this lowercases stuff, TODO: Generalize this so it doesn't need lowercasing
    """
    sent = str(sent).lower().strip()
    arr_w = w(sent)
    idx_tail = len(arr_w)
    markers = []
    for idx_beg in range(idx_tail):
        for idx_end in range(idx_beg + 1, idx_tail +1):
            next_values = seq.look_ahead(encode_from_word_list(arr_w[idx_beg:idx_end])).get_next_values()
            matches = list(set(next_values) & set(lst_targets) )
            if matches:
                markers.append([idx_beg, idx_end, idx_end - idx_beg, matches, ' '.join(arr_w[idx_beg:idx_end])])
    return markers


def return_max_address(seq, sent):
    sent = str(sent).lower().strip()
    arr_cands = get_markers(seq, sent, ['ADDRESS'])
    if not arr_cands:
        return str([encoder(word) for word in w(sent)])

    max_len = 0
    for cand in arr_cands:
        if cand[2] > max_len:
            max_len = cand[2]
            candidate_address = cand[4]

    candidate_address = candidate_address.upper()
    if candidate_address != sent.upper():
        return 'DIFF!! {} | {}'.format(str([encoder(word, trim=True) for word in w(sent)]), candidate_address)
    else:
        return candidate_address


if __name__ == "__main__":
    #################################################################################
    import pandas as pd
    df = pd.read_csv('originals.csv')
    df_addresses = df[['ACCT_STREET_ADDR']]
    df_addresses.drop_duplicates(keep='first', inplace=True)
    df_addresses['NEW ADDRESS'] = df_addresses['ACCT_STREET_ADDR'].apply(lambda x: return_max_address(seq, x))
    df_addresses.to_csv('processed_addresses.csv')
    os.system("open 'processed_addresses.csv'")
