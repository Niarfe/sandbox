import csv
import sys
sys.path.append('.')

import phrase_entity_extraction as pext


def test_markers():
    marker_lengths = [
        ("123 main st", 2),
        ("901 s bolmar st # a", 3),
    ]
    for address, length in marker_lengths:
        assert len(pext.get_markers(pext.seq, address, ['ADDRESS'])) == length, "{} should have {} markers".format(address, length)

def test_basics():
    valid_addresses = [
        "123 MAIN ST",
        "901 S BOLMAR ST # A",
        "300 PHOENIX MILLS PLZ"
    ]

    for address in valid_addresses:
        assert pext.return_max_address(pext.seq, address) == address.upper(), address

def test_pobox():
    sent = "po box 7001"
    assert pext.is_pobox(pext.seq, pext.w(sent)) == True

def test_attn():
    sent = "attn john doe"
    assert pext.is_deleg(pext.seq, pext.w(sent)) == True

def test_suite():
    sent = "ste c"
    assert pext.is_suite(pext.seq, pext.w(sent)) == True

def test_multiple_markers():
    marker_lengths = [
        ("123 main st", 2),
        ("901 s bolmar st # a", 3),
        ("123 main st c/o gustav mahler", 4)
    ]
    for address, length in marker_lengths:
        assert len(pext.get_markers(pext.seq, address, ['ADDRESS', 'ATTN'])) == length, "{} should have {} markers".format(address, length)

def _load_column(path_file, column):
    with open(path_file, 'r') as source:
        csv_file = csv.DictReader(source)
        return [row[column] for row in csv_file]


def test_base_addresses():
    base_addresses = _load_column('data/address_bases.csv', 'ADDRESSES')

    for base_address in base_addresses:
        assert pext.return_max_address(pext.seq, base_address) == base_address.upper(), "{} should be a base address".format(base_address)

def test_base_suites():
    base_suites = _load_column('data/address_suite.csv', 'ADDRESSES')

    for base_suite in base_suites:
        assert pext.is_suite(pext.seq, pext.w(base_suite.lower())) == True, base_suite.upper()