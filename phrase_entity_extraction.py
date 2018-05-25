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
def encoder(word, trim=False):
    encodings = [
        ('POBOX', [r'^:box$']),
        ('LETTER', [r'^[a-z]$']),
        ('ALNUM', [r'^(\d+[a-z]+|[a-z]+\d+)[\da-z]*$']),
        ('AL_1NUM', [ r'^\d+[a-z]$' ]),
        ('NTH',    [ nths ]),
        ('ATTN', [r'^:deleg$']),
        ('WAY',  [ ways ]),
        ('DIR',  [ dirs ]),
        ('NUMSTR', [r'^\d+[a-z]+$' ]),
        ('APT', [ apts ]),
        ('DIGIT', [r'^\d+$']),
        ('COMMA', [r'^,$']),
        ('PERIOD', [r'^\.$']),
        ('POUND', [r'^#$']),
        ('DELEG', [r'^attn$', r'^attn:$', r'^c\/o$', r'^co$' ]),
        ('POB0', [r'^po$', r'^p\.o\.$']),
        ('POB2', [r'^box$']),
        ('PRE',  [ pre ]),
        ('ARTI', [ arti ]),
        ('ADDRESS', [r'^:adr$']),
        ('ALPHA', [r'^[a-z]+$']),
    ]
    if not trim:
        return [key for key, rexs in encodings for rex in rexs if re.match(rex, word)]
    else:
        encoding = [key for key, rexs in encodings for rex in rexs if re.match(rex, word)]
        if len(encoding) > 1 and 'ALPHA' in encoding:
            encoding.remove('ALPHA')
        if len(encoding) > 1 and 'ALNUM' in encoding:
            encoding.remove('ALNUM')
        return encoding

# THOU SHALL NOT SEQUENCE THREE ALPHAS IN A ROW!
def train_with_provided_list(seq, matrix_lst):
    """matrix list means [['DIGIT'],['ALPHA'],['WAY']] for example"""
    return seq.insert(matrix_lst, is_learning=True).get_next_values()

tuples_training = [
    ("123 main st",                    [['DIGIT'], ['ALPHA'], ['WAY']]),
    ("1217 iris ct",                   [['DIGIT'], ['ALPHA'], ['WAY']]),
    ("123 east main st",               [['DIGIT'], ['DIR'], ['ALPHA'], ['WAY']]),
    ("310 W MAIN ST",                  [['DIGIT'], ['DIR'], ['ALPHA'], ['WAY']]),
    ("123 south main street.",         [['DIGIT'], ['DIR'], ['ALPHA'], ['WAY'], ['PERIOD']]),
    ("90 south park rd",               [['DIGIT'], ['DIR'], ['ALPHA'], ['WAY']]),
    ("987 el canyon ave",              [['DIGIT'], ['ARTI'], ['ALPHA'], ['WAY']]),
    ("333 st james st",                [['DIGIT'], ['PRE'], ['ALPHA'], ['WAY']]),
    ("123 west hill",                  [['DIGIT'], ['DIR'], ['ALPHA']]),
    ("77 el camino real",              [['DIGIT'], ['ARTI'], ['ALPHA'], ['ALPHA']]),
    ("1 bay st # b",                   [['DIGIT'], ['ALPHA'], ['WAY'], ['POUND'], ['LETTER']]),
    ("1 bay rd # b",                   [['DIGIT'], ['ALPHA'], ['WAY'], ['POUND'], ['LETTER']]),
    ("43 HUDSON AVE # 2",              [['DIGIT'], ['ALPHA'], ['WAY'], ['POUND'], ['DIGIT']]),
    ("111 san vicente blvd",           [['DIGIT'], ['PRE'], ['ALPHA'], ['WAY']]),
    ("28 black watch way",             [['DIGIT'], ['ALPHA'], ['ALPHA'], ['WAY']]),
    ("249 route 206",                  [['DIGIT'], ['WAY'], ['DIGIT']]),
    ("5500 lost tree",                 [['DIGIT'], ['ALPHA'], ['ALPHA']]),
    ("996 san benito st",              [['DIGIT'], ['PRE'], ['ALPHA'], ['WAY']]),
    ("899 embarcadero",                [['DIGIT'], ['ALPHA']]),
    ("177 montague e",                 [['DIGIT'], ['ALPHA'], ['DIR']]),
    ("2001 W COURT ST",                [['DIGIT'], ['DIR'], ['ALPHA'], ['WAY']]),
    ("12545 S HIGHWAY J",              [['DIGIT'], ['DIR'], ['WAY'], ['LETTER']]),
    ("437 S HIGHWAY 101 STE 501",      [['DIGIT'], ['DIR'], ['WAY'], ['DIGIT'], ['APT'], ['DIGIT']]),
    ("12940 S HIGHWAY 259",            [['DIGIT'], ['DIR'], ['WAY'], ['DIGIT']]),
    ("775 E 14 MILE RD",               [['DIGIT'], ['DIR'], ['DIGIT'], ['ALPHA'], ['WAY']]),
    ("4701 VAN DAM ST",                [['DIGIT'], ['ALPHA'], ['ALPHA'], ['WAY']]),
    ("3201 NEW MEXICO AVE NW STE 246", [['DIGIT'], ['ALPHA'], ['ALPHA'], ['WAY'], ['DIR'], ['APT'], ['DIGIT']]),
    ("111 RIO RANCHO BLVD SE",         [['DIGIT'], ['ALPHA'], ['ALPHA'], ['WAY'], ['DIR']]),
    ("17259 WILD HORSE CREEK RD",      [['DIGIT'], ['ALPHA'], ['ALPHA'], ['ALPHA'], ['WAY']]),
    ("12587 FAIR LAKES CIR STE 141",   [['DIGIT'], ['ALPHA'], ['ALPHA'], ['WAY'], ['APT'], ['DIGIT']]),
    ("107 E MARIPOSA DR",              [['DIGIT'], ['DIR'], ['ALPHA'], ['WAY']]),
    ("401 W FORT WILLIAMS ST",         [['DIGIT'], ['DIR'], ['ALPHA'], ['ALPHA'], ['WAY']]),
    ("3242 E DESERT INN RD STE 17",    [['DIGIT'], ['DIR'], ['ALPHA'], ['ALPHA'], ['WAY'], ['APT'], ['DIGIT']]),
    ("14238 44ND AVE",                 [['DIGIT'], ['NUMSTR'], ['WAY']]),
    ("106 HARVEST HILL LN",            [['DIGIT'], ['ALPHA'], ['ALPHA'], ['WAY']]),
    ("206 ELMHURST DR APT F15",        [['DIGIT'], ['ALPHA'], ['WAY'], ['APT'], ['ALNUM']]),
    ("655 COUNTY ROAD 1300",           [['DIGIT'], ['ALPHA'], ['WAY'], ['DIGIT']]),
    ("50 LOS PATOS WAY",               [['DIGIT'], ['ARTI'], ['ALPHA'], ['WAY']]),
    ("1001 N 60TH ST",                 [['DIGIT'], ['DIR'], ['NUMSTR'], ['WAY']]),
    ("5350 S SANTA FE DR",             [['DIGIT'], ['DIR'], ['ALPHA'], ['ALPHA'], ['WAY']]),
    ("638 18TH ST",                    [['DIGIT'], ['NUMSTR'], ['WAY']]),
    ("210 E 3RD AVE",                  [['DIGIT'], ['DIR'], ['NUMSTR'], ['WAY']]),
    ("1390 SW 160TH AVE",              [['DIGIT'], ['DIR'], ['NUMSTR'], ['WAY']]),
    ("171 NE 212TH ST",                [['DIGIT'], ['DIR'], ['NUMSTR'], ['WAY']]),
    ("712 B MAIN ST",                  [['DIGIT'], ['LETTER'], ['ALPHA'], ['WAY']]),
    ("2060 B MOUNTAIN BLVD",           [['DIGIT'], ['LETTER'], ['ALPHA'], ['WAY']]),
    ("123 avenue c",                   [['DIGIT'], ['WAY'], ['LETTER']]),
    ("717B GRAVES ST",                 [['ALNUM'], ['ALPHA'], ['WAY']]),
    ("1234 7TH AVENUE",                [['DIGIT'], ['NTH'], ['WAY']]),
    ("205 3RD AVE APT 3K",             [['DIGIT'], ['NTH'], ['WAY'], ['APT'], ['ALNUM']]),
    ("462 7TH AVE FL 2",               [['DIGIT'], ['NTH'], ['WAY'], ['ALPHA'], ['DIGIT']]),
    ("219 2ND AVE SE STE 101",         [['DIGIT'], ['NTH'], ['WAY'], ['DIR'], ['APT'], ['DIGIT']]),
    ("10859 12TH AVE SW",              [['DIGIT'], ['NTH'], ['WAY'], ['DIR']]),
    ("4401 LOOP 322",                  [['DIGIT'], ['ALPHA'], ['DIGIT']]),
    ("8690 EDGE OF TEXAS",             [['DIGIT'], ['ALPHA'], ['ARTI'], ['ALPHA']]),
    ("487 RITCHIE HWY B102",           [['DIGIT'], ['ALPHA'], ['WAY'], ['ALNUM']]),
    ("366 RAILROAD AVE LOT 31",        [['DIGIT'], ['ALPHA'], ['WAY'], ['APT'], ['DIGIT']]),
    ("1631A S MAIN ST",                [['AL_1NUM'],['DIR'],['ALPHA'],['WAY']]),
    ("338A 7TH AVE",                   [['AL_1NUM'],['NTH'],['WAY']]),
    ("1771A PRINCESS ANNE RD",         [['AL_1NUM'], ['ALPHA'], ['ALPHA'], ['WAY']]),
    ("751 ROUTE 37 W",                 [['DIGIT'], ['WAY'], ['DIGIT'], ['DIR']]),
    ("73140 HIGHWAY 111 STE 6",        [['DIGIT'], ['WAY'], ['DIGIT'], ['APT'], ['DIGIT']]),
    ("476534 HIGHWAY 95 STE A",        [['DIGIT'], ['WAY'], ['DIGIT'], ['APT'], ['LETTER']]),
    ("225 LA PALOMA APT A",            [['DIGIT'], ['ARTI'], ['ALPHA'], ['APT'], ['LETTER']]), # DIFF!
    ("3200 SISK RD STE C",             [['DIGIT'], ['ALPHA'], ['WAY'], ['APT'], ['LETTER']]), # DIFF!
    ("2584 US HIGHWAY 80 W",           [['DIGIT'], ['ALPHA'], ['WAY'], ['DIGIT'], ['DIR']]), # DIFF!
    ("2387 PORTOLA RD STE A",          [['DIGIT'], ['ALPHA'], ['WAY'], ['APT'], ['LETTER']]), # DIFF!
    ("118 N 300 W",                    [['DIGIT'], ['DIR'], ['DIGIT'], ['DIR']]),
    ("1027 S WESTERN AVE # 2",         [['DIGIT'], ['DIR'], ['ALPHA'], ['WAY'], ['POUND'], ['DIGIT']]),
    ("690 S STATE HIGHWAY 5",          [['DIGIT'], ['DIR'], ['ALPHA'], ['WAY'], ['DIGIT']]),
    ("3070 W CHAPMAN AVE STE A",       [['DIGIT'], ['DIR'], ['ALPHA'], ['WAY'], ['APT'], ['LETTER']]),
    ("1420 E PLAZA BLVD STE D5",       [['DIGIT'], ['DIR'], ['ALPHA'], ['WAY'], ['APT'], ['ALNUM']]),
    ("82 S MAIN ST # 2",               [['DIGIT'], ['DIR'], ['ALPHA'], ['WAY', 'PRE'], ['POUND'], ['DIGIT']]),
    ("473 S MAIN ST STE A",            [['DIGIT'], ['DIR'], ['ALPHA'], ['WAY'], ['APT'], ['LETTER']]),
    ("1029 W BATTLEFIELD ST APT E214", [['DIGIT'], ['DIR'], ['ALPHA'], ['WAY', 'PRE'], ['APT'],['ALNUM']]),
    ("3843 S BRISTOL 213",             [['DIGIT'], ['DIR'], ['ALPHA'], ['DIGIT']]),
]
for ts, matrix_lst in tuples_training:
    matrix_lst.append(['ADDRESS'])
    train_with_provided_list(seq, matrix_lst)

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

sent = "po box 7001"
assert is_pobox(seq, w(sent)) == True

def is_deleg(seq, arr_st):
    """Expects ["123","main","st"]"""
    assert isinstance(arr_st, list)
    return any([pred == 'ATTN' for pred in seq.look_ahead(encode_from_word_list(arr_st)).get_next_values()])

sent = "attn john doe"
assert is_deleg(seq, w(sent)) == True


def get_markers(seq, sent, lst_targets):
    """Input is like '123 main str' and returns a list of lists"""
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


#st = "c/o john smith 100 maple ave"
st = "333 st james st"
get_markers(seq, st, ['ADDRESS'])

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
        return '("", {}),'.format(str([encoder(word, trim=True) for word in w(sent)]))
    else:
        return candidate_address

return_max_address(seq, "16w661 90th st")

#################################################################################
import pandas as pd
df = pd.read_csv('originals.csv')
df_addresses = df[['ACCT_STREET_ADDR']]
df_addresses.drop_duplicates(keep='first', inplace=True)
df_addresses['NEW ADDRESS'] = df_addresses['ACCT_STREET_ADDR'].apply(lambda x: return_max_address(seq, x))
df_addresses.to_csv('processed_addresses.csv')
os.system("open 'processed_addresses.csv'")
