import os
import re
from hydraseq import Hydraseq


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

def w(str_sentence):
    return re.findall(r"[\w'/\-:#]+|[,!?&]", str_sentence)

seq = Hydraseq('input')
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
    rex_gigit_direction = r'^\d+[nsew]{1,2}'
    rex_digdashal = r'^\d+-[a-z]+$'
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
            ('WAYCOKY',      [ r'^county$', r'^co$', r'^ky$' ]), # county and co show up in '123 CO RD 456'
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
        ('ADR_HEAD',        [r'^\d+$', word_numbers, r'^[nsew]\d+$', r'^#\d+$', r'\d+-\d+$', r'^[nsew]\d+[nsew]\d+$', rex_gigit_direction, rex_digdashal ]),
        ('ALNUM',           [r'^(\d+[a-z]+|[a-z]+\d+)[\da-z]*$']),
            ('DIGDASHAL',   [r'^\d+-[a-z]+$'] ),
            ('BOXNUM',      [r'^box\d+$']),
            ('ALDASHDIG',   [r'^[a-z]+-\d+$'] ),
            ('NUMSTR',      [r'^\d+[a-z]+$' ]),
                ('NTH',     [ nths, r'^[nsew]\d+(rd|st|th)' ]),
                ('NUMS_1AL',[ r'^\d+[a-z]$' ]),
                ('APT_NUM', [ r'^' + apts_base + r'\d+$', r'^' + apts_base + r'[a-z]$' ]),

        # SYMBOLS ONLY
        ('COMMA',           [r'^,$']),
        ('PERIOD',          [r'^\.$']),
        ('POUND',           [r'^#$']),

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
        if any([key in ['P','O','NEGATIVE', 'TH','SP_ARTI','LETTER', 'WORDWAY', 'WAY', 'APT', 'ARTI', 'PRE', 'DIR', 'DELEG', 'POB2', 'POB0', 'FARM2MARK'] for key in encoding]) and 'ALPHA' in encoding:
            encoding.remove('ALPHA')  # Redudant category level if we have probable meaning
        if any([key in ['NUMS_1AL', 'NUMSTR', 'NTH'] for key in encoding]) and 'ALNUM' in encoding:
            encoding.remove('ALNUM')  # Redudant category level if we have probable meaning
        if any([key in ['NUMS_1AL', 'NTH'] for key in encoding]) and 'NUMSTR' in encoding:
            encoding.remove('NUMSTR')

        return encoding



# THOU SHALL NOT SEQUENCE THREE ALPHAS IN A ROW!
def train_with_provided_list(seq, matrix_lst):
    """matrix list means [['DIGIT'],['ALPHA'],['WAY']] for example"""
    #print(matrix_lst)
    return seq.insert(matrix_lst, is_learning=True).get_next_values()


import csv
suite_sequences = []
with open('data/address_suite.csv', 'r') as source:
    csv_file = csv.DictReader(source)
    for row in csv_file:
        lst_sequence = eval(row['SEQUENCE'])
        train_with_provided_list(seq, lst_sequence + [['SUITE']])
        suite_sequences.append(lst_sequence)

with open('data/address_bases.csv', 'r') as source:
    csv_file = csv.DictReader(source)
    for row in csv_file:
        lst_sequence = eval(row['SEQUENCE'])
        #print("==PLAIN")
        train_with_provided_list(seq, lst_sequence + [['ADDRESS']])  # THIS IS THE PLAIN ADDRESS SEQUENCE
        # for suite_sequence in suite_sequences:
        #     #print("==== >>>>")
        #     train_with_provided_list(seq, lst_sequence + suite_sequence + [['ADDRESS']])
        # for suite_sequence in suite_sequences:
        #     #print("<<<< ====")
        #     train_with_provided_list(seq, suite_sequence + lst_sequence + [['ADDRESS']])
train_with_provided_list(seq, [['DIR'],['_DIR_']])

# import sys
# sys.exit(0)

# valid po box
train_samples = [
    ("po box 1234",     [['POB0'],['POB2'],['DIGIT']]),
    ("po box1234",      [['POB0'], ['BOXNUM']]),
    ("po drawer 1234",  [['POB0'],['DRAWER'],['DIGIT']]),
    ("po box #1234",    [['POB0'],['POB2'],['POUNDDIG']]),
    ("PO BOX E",        [['POB0'], ['POB2'], ['LETTER']]),
    ("box 999",         [['POB2'],['DIGIT']]),
    ("post box 999",    [['POST'],['POB2'],['DIGIT']]),
    ("pobox 999",       [['POBOX1'],['DIGIT']]),
    ("p o box 123",     [['POST'], ['OFFICE'], ['POB2'], ['DIGIT']]),
    ("p o drawer 123",  [['POST'], ['OFFICE'], ['DRAWER'], ['DIGIT']]),
    ("PO BOX 1570A",    [['POB0'], ['POB2'], ['NUMS_1AL']]),
    ("HC 65 BOX 5008",  [['POBHC'],['DIGIT'],['POB2'],['DIGIT']]),  # https://ribbs.usps.gov/cassmassguidelines/CASS%20and%20MASS%20Guidelines/508Version/address_match_sec10_examples.htm
    ("RR 11 BOX 100",   [['POBHC'],['DIGIT'],['POB2'],['DIGIT']]),   # same ^^
    ("PO BOX RKM",      [['POB0'], ['POB2'], ['ALPHA']]),
    ("PO BOX C-847",    [['POB0'], ['POB2'], ['ALDASHDIG']]),
    ("PO BOX 5041IG",   [['POB0'], ['POB2'], ['NUMSTR']]),
    ("PO BOX 3277-CRS", [['POB0'], ['POB2'], ['DIGDASHAL']]),
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

def is_suite(seq, st):
    """Expects ["123","main","st"]"""
    assert isinstance(st, str)
    return any([pred == 'SUITE' for pred in seq.look_ahead(encode_from_word_list(w(st))).get_next_values()])

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

def get_best_fit(seq, sent, lst_targets):
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

    greedy_match = {}
    for target in lst_targets:
        greedy_match[match] = [match for match in markers if target in match[4]]

    return greedy_match



def return_max_sequence(seq, sent, arr_cands, entity):
    sent = str(sent).lower().strip()
    arr_cands = arr_cands #[arr_cand for arr_cand in arr_cands if arr_cand[4] == entity]
    if not arr_cands:
        print("NOTHING HERE")
        return str([encoder(word) for word in w(sent)])

    max_len = 0
    for cand in arr_cands:
        if cand[2] > max_len:
            max_len = cand[2]
            candidate_address = cand[4]

    candidate_address = candidate_address.upper()
    if candidate_address != sent.upper():
        return '{}'.format(str([encoder(word, trim=True) for word in w(sent)]))
    else:
        return candidate_address


def return_max_address(seq, sent):
    sent = str(sent).lower().strip()
    sent = re.sub(r'\s+', ' ', sent)
    arr_cands = get_markers(seq, sent, ['ADDRESS', 'POBOX'])
    if not arr_cands:
        return str(encode_from_word_list(w(sent)))

    max_len = 0
    for cand in arr_cands:
        if cand[2] > max_len:
            max_len = cand[2]
            candidate_address = cand[4]

    candidate_address = candidate_address.upper()
    if False: #candidate_address != sent.upper():
        return '{}'.format(str([encoder(word, trim=True) for word in w(sent)]))
    else:
        return candidate_address


### %% NEW SECOND LEVEL
def get_interpretation(seq, arr_words, arr_search_keys):
    """INPUT: ['123', 'main']"""
    t1_encoded = encode_from_word_list(arr_words)
    #print("encoded: " ,t1_encoded)
    seq.look_ahead(t1_encoded)
    next_values = seq.get_next_values()
    #print("returning ", next_values)
    return [search_key for search_key in arr_search_keys if search_key in next_values]


def index_tail(lst):
    """Return the 0 based index of last element in lst"""
    return len(lst) - 1
def validate_back_jump(last_length, idx):
    """Validate jumping back to start of sequence, check if any other back sequence is in the way"""
    current_range = last_length[idx]
    while current_range > 1:
        #print("index: ", idx, " range: ", current_range, " last ", last_length[idx-1], " <? ", current_range -1)
        if last_length[idx-1] <= current_range - 1:
            current_range -= 1
            idx -= 1
            continue
        else:
            return False
    return True

def decompose_into_dictionary_words(domain, _seq, types):
    last_length = [-1] * len(domain)
    last_interp = ['']*len(domain)

    for i in range(len(domain)):
        inter1 = get_interpretation(_seq, domain[:i + 1], types)
        if any([ret_type in types for ret_type in inter1]):
            last_interp[i] = [hit for hit in inter1 if hit in types]
            last_length[i] = i + 1

        if last_length[i] == -1:
            for j in range(i):
                inter2 = get_interpretation(_seq, domain[j + 1:i + 1], types)
                if any([ret_type in types for ret_type in inter2]):
                    last_interp[i] = [hit for hit in inter2 if hit in types]
                    last_length[i] = i - j
                    break
    print(last_length)
    decompositions = []
    components = []
    idx = index_tail(domain)
    while idx >= 0:
        if validate_back_jump(last_length, idx):
            decompositions.append(last_interp[idx])
            components.append((last_interp[idx], " ".join(domain[idx + 1 - last_length[idx]:idx + 1])))
        if last_length[idx] == -1:
            idx -= 1
            continue
        if validate_back_jump(last_length, idx):
            idx -= last_length[idx]
        else:
            idx -= 1
    decompositions = decompositions[::-1]
    components = components[::-1]
    return last_length, last_interp, decompositions, components


def return_max_address2(seq, sent):
    kinds = ['ADDRESS', 'POBOX', 'SUITE']
    decomposition = decompose_into_dictionary_words(w(sent.lower()), seq, kinds)
    found_tuples = decomposition[3]
    max_address = []
    for kindof, value in found_tuples:
        if kindof and kindof[0] in kinds:
            max_address.append(value)
    return " ".join(max_address).upper()

### SUPER HYDRA ACTION!
def return_best_fit(seq, sent, book_fit=True):
    items_of_interest = ['POBOX', 'ADDRESS', 'ATTN', 'SUITE','_DIR_']
    markers = get_markers(seq, sent, items_of_interest)
    def get_sorted_entity(_markers, entity):
        entities = [arr for arr in _markers if arr[3][0] == entity]
        entities.sort(key=lambda x: int(x[2]))
        return entities

    def entitys_overlap(ent1, ent2):
        if ent1[1] <= ent2[0] or ent2[1] <= ent1[0]:
            return False
        else:
            return True

    def add_next(markers, best_fit, entity):
        """Check markers of type 'entity' and push into best_fit if it doesn't overlap with existing"""
        sorted_markers = get_sorted_entity(markers, entity)
        if entity == 'ADDRESS' and len(sorted_markers) > 1:
            max_len = sorted_markers[-1][2]
            #print("max len", max_len)
            #print("A",sorted_markers)
            sorted_markers = [marker for marker in sorted_markers if marker[2] == max_len] # keep only large ones
            sorted_markers.sort(key=lambda x: int(x[0]))
            #print("B",sorted_markers)
            sorted_markers = sorted_markers[::-1]
        idx = len(sorted_markers) - 1
        while idx >= 0:
            if not any([entitys_overlap(item, sorted_markers[idx]) for item in best_fit]):
                #print("C",sorted_markers)
                best_fit.append(sorted_markers[idx])
                break
            else:
                idx -= 1
        return best_fit

    def book_best_fit(arr_domain, markers):
        def is_in_dictionary(markers, start, endplus):
            match_starts = [item for item in markers if item[0] == start]
            match_both = [item for item in match_starts if item[1] == endplus]
            return match_both
        last_length = [-1]*len(arr_domain)
        for i in range(len(arr_domain)):
            if is_in_dictionary(markers, 0, i+1):
                last_length[i] = i + 1
            if last_length[i] == -1:
                for j in range(i):
                    if last_length[j] != -1 and is_in_dictionary(markers, j+1, i+1):
                        last_length[i] = i - j
                        break
        decompositions = []
        if last_length[-1] != -1:
            idx = len(arr_domain) - 1
            while idx >= 0:
                decompositions.append(is_in_dictionary(markers,idx + 1 - last_length[idx], idx + 1)[0])
                idx -= last_length[idx]
            decompositions = decompositions[::-1]
        return decompositions

    best_fit = []
    if book_fit:
        best_fit = book_best_fit(w(sent), markers)
        if best_fit:
            return best_fit

    for nugget in items_of_interest:
        best_fit = add_next(markers, best_fit, nugget)
        best_fit.sort(key=lambda x: int(x[0]))

    return best_fit


def return_max_address3(seq, sent):
    results = return_best_fit(seq,sent)
    if not results:
        return ''

    addresses = [result[4] for result in results if result[3][0] in ['ADDRESS', 'SUITE','_DIR_']]

    if not addresses:
        addresses = [result[4] for result in results if result[3][0] in ['POBOX']]

    address = " ".join(addresses)
    return address.upper()

if __name__ == "__main__":
    #################################################################################
    import pandas as pd
    df = pd.read_csv('data/badboys.csv')
    df_addresses = df[['ACCT_STREET_ADDR']]
    df_addresses.drop_duplicates(keep='first', inplace=True)
    df_addresses['NEW ADDRESS'] = df_addresses['ACCT_STREET_ADDR'].apply(lambda x: return_max_address(seq, x))
    df_addresses.to_csv('processed.csv')
    os.system("open 'processed.csv'")
