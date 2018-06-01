import csv
import sys
import pytest
sys.path.append('.')

import phrase_entity_extraction as pext


def _load_column(path_file, column):
    with open(path_file, 'r') as source:
        csv_file = csv.DictReader(source)
        return [row[column] for row in csv_file]

def _load_csv_file(path_file):
    with open(path_file, 'r') as source:
        csv_file = csv.DictReader(source)
    return csv_file


def test_base_addresses():
    base_addresses = _load_column('data/address_bases.csv', 'ADDRESSES')

    for base_address in base_addresses:
        assert pext.return_max_address3(pext.seq, base_address) == base_address.upper(), "{} should be a base address".format(base_address)

def test_known_bad_addresses():
    base_addresses = _load_column('data/known_good/known_bad_addresses.csv', 'ADDRESSES')

    for base_address in base_addresses:
        returned_string = pext.return_max_address(pext.seq, base_address)
        assert returned_string.startswith("[")
        assert returned_string.endswith("]")

def test_known_good_pobox_addresses():
    poboxs = _load_column('data/known_good/known_pobox.csv', 'ADDRESSES')

    for pobox in poboxs:
        assert pext.return_max_address3(pext.seq, pobox) == pobox.upper(), "{} should be a pobox address".format(pobox)

def test_known_good_full_clean_addresses():
    base_addresses = _load_column('data/known_good/full_clean_addresses.csv', 'ADDRESSES')

    for base_address in base_addresses:
        assert pext.return_max_address3(pext.seq, base_address) == base_address.upper(), '{},"{}"'.format(base_address.upper(), pext.encode_from_word_list(pext.w(base_address.lower())))

@pytest.mark.skip
def test_eighty_k_good_street_and_po_samples():
    base_addresses = _load_column('data/known_good/eighty_k_good_street_and_po_samples.csv', 'ADDRESSES')

    for base_address in base_addresses:
        assert pext.return_max_address3(pext.seq, base_address) == base_address.upper(), '{},"{}"'.format(base_address.upper(), pext.encode_from_word_list(pext.w(base_address.lower())))

