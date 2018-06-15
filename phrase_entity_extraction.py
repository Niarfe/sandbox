import csv
import os
import re
from hydraseq import Hydraseq
import phrase_entity_encoder as pee



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
    str_sentence = str(str_sentence)
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



# THOU SHALL NOT SEQUENCE THREE ALPHAS IN A ROW!
def train_with_provided_list(seq, matrix_lst):
    """matrix list means [['DIGIT'],['ALPHA'],['WAY']] for example"""
    return seq.insert(matrix_lst, is_learning=True).get_next_values()


def train_sequences_from_file(_seq, filepath, lst_lst_identifier):
    """Insert training sequences from stored file.
        _seq    - a live Hydra sequencer to train
        filepath    - csv two column file, second column 'SEQUENCE' contains lists of lists
        lst_lst_identifier  - what identifier to use to cap seqennces, [['mysequence']] for example
    """
    with open(filepath, 'r') as source:
        csv_file = csv.DictReader(source)
        for row in csv_file:
            str_sequence = row['SEQUENCE'].strip()
            if len(str_sequence.strip()) == 0:
                continue
            else:
                #print("::",str_sequence)
                lst_sequence = eval(str_sequence)
                train_with_provided_list(_seq, lst_sequence + lst_lst_identifier)

train_sequences_from_file(seq, 'data/address_suite.csv', [['_SUITE_']])
train_sequences_from_file(seq, 'data/address_bases.csv', [['_ADDRESS_']])
train_with_provided_list(seq, [['DIR'],['_DIR_']])
train_sequences_from_file(seq, 'data/address_poboxs.csv', [['_POBOX_']])




# valid attn
train_samples = [
    ("c/o john smith",              [['DELEG'],['ALPHA'],['ALPHA']]),
    ("attn john smith",             [['DELEG'],['ALPHA'],['ALPHA']]),
    ("attn: john smith",            [['DELEG'],['ALPHA'],['ALPHA']]),
    ("c/o john", [['DELEG'],        ['ALPHA']]),
    ("c/o dell&schaefer law firm",  [['DELEG'], ['ALPHA'], ['AND'], ['ALPHA'], ['ALPHA'], ['ALPHA']]),
]
for ts, matrix_lst in train_samples:
    matrix_lst.append(['_ATTN_'])
    train_with_provided_list(seq, matrix_lst)

def encode_from_word_list(arr_st):
    """Expects ['123', 'main', 'st]"""
    assert isinstance(arr_st, list)
    if arr_st: assert isinstance(arr_st[0], str)
    return [encoder(word) for word in arr_st]

def is_address(seq, arr_st):
    """Expects ["123","main","st"]"""
    return any([pred == '_ADDRESS_' for pred in seq.look_ahead(encode_from_word_list(arr_st)).get_next_values()])

def is_pobox(seq, arr_st):
    """Expects ["123","main","st"]"""
    assert isinstance(arr_st, list)
    return any([pred == '_POBOX_' for pred in seq.look_ahead(encode_from_word_list(arr_st)).get_next_values()])


def is_deleg(seq, arr_st):
    """Expects ["123","main","st"]"""
    assert isinstance(arr_st, list)
    return any([pred == '_ATTN_' for pred in seq.look_ahead(encode_from_word_list(arr_st)).get_next_values()])

def is_suite(seq, st):
    """Expects ["123","main","st"]"""
    assert isinstance(st, str)
    return any([pred == '_SUITE_' for pred in seq.look_ahead(encode_from_word_list(w(st))).get_next_values()])

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











### DOUBLE DECKER APPROACH
def return_max_address4(seq, sent):
    markers = get_markers(seq, sent, ['_ADDRESS_', '_POBOX_', '_SUITE_', '_DIR_'])
    class BreathFirstSearch:
        def __init__(self, markers):
            self.markers = markers
        def end(self, node):
            return node[1]
        def start(self, node):
            return node[0]
        def type(self, node):
            return node[3][0]
        def length(self, node):
            return node[2]
        def rep(self, node):
            return node[4]
        def get_successors(self, current_node):
            next_matches = [n for n in self.markers if self.start(n) == self.end(current_node) and self.type(n) != self.type(current_node) and self.type(n) != '_POBOX_']
            return next_matches[:]
        def get_branches(self, node):
            fringe = [[node[:]]]
            branches = []
            while fringe:
                activeNode = fringe.pop()
                successors = self.get_successors(activeNode[-1])
                if successors:
                    for successor in successors:
                        nextNode = activeNode[:]
                        nextNode.append(successor)
                        fringe.append(nextNode[:])
                else:
                    branches.append(activeNode)
            return branches
        def get_all_branches(self):
            all_branches = []
            for node in self.markers:
                for branch in self.get_branches(node):
                    all_branches.append(branch)
            return all_branches

    bfs = BreathFirstSearch(markers)
    seq2 = Hydraseq('second')
    seq2.insert("_SUITE_ _ADDRESS_ *KEEP*")
    seq2.insert("_ADDRESS_ *KEEP*")
    seq2.insert("_ADDRESS_ _SUITE_ *KEEP*")
    seq2.insert("_ADDRESS_ _DIR_ *KEEP*")
    seq2.insert("_ADDRESS_ _DIR_ _SUITE_ *KEEP*")
    seq2.insert("_POBOX_ *KEEP*")
    keepers = [branch for branch in bfs.get_all_branches() if 'KEEP' in seq2.look_ahead([node[3] for node in branch] ).get_next_values()]

    max_len = 0
    max_branch = None
    for branch in keepers:
        len_branch = branch[-1][1] - branch[0][0]
        if len_branch > max_len:
            max_len = len_branch
            max_branch = branch

    #print("HERE: ",max_branch)
    return " ".join([item[4] for item in max_branch])

if __name__ == "__main__":
    #################################################################################
    import pandas as pd
    df = pd.read_csv('data/badboys.csv')
    df_addresses = df[['ACCT_STREET_ADDR']]
    df_addresses.drop_duplicates(keep='first', inplace=True)
    df_addresses['NEW ADDRESS'] = df_addresses['ACCT_STREET_ADDR'].apply(lambda x: return_max_address(seq, x))
    df_addresses.to_csv('processed.csv')
    os.system("open 'processed.csv'")
