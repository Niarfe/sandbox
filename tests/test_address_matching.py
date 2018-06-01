import csv
import sys
sys.path.append('.')

import phrase_entity_extraction as pext


def test_markers():
    marker_lengths = [
        ("123 main st", 2),
        ("901 s bolmar st # a", 2),
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
        assert pext.return_max_address2(pext.seq, address) == address.upper(), address

def test_pobox():
    sent = "po box 7001"
    assert pext.is_pobox(pext.seq, pext.w(sent)) == True

def test_attn():
    sent = "attn john doe"
    assert pext.is_deleg(pext.seq, pext.w(sent)) == True


def test_multiple_markers():
    marker_lengths = [
        ("123 main st", 2),
        ("901 s bolmar st # a", 2),
        ("123 main st c/o gustav mahler", 4)
    ]
    for address, length in marker_lengths:
        assert len(pext.get_markers(pext.seq, address, ['ADDRESS', 'ATTN'])) == length, "{} should have {} markers".format(address, length)


def test_incompletes():
    incompletes = [
        ("2010 OLD MONTGOMERY HWY SUITE",    "2010 OLD MONTGOMERY HWY"),
        ("731 PLEASANT GROVE BLVD SUITE",    "731 PLEASANT GROVE BLVD"),
        ("8690 SIERRA COLLEGE BLVD STE",     "8690 SIERRA COLLEGE BLVD"),
        ("4000 VIRGINIA BEACH BLVD STE",     "4000 VIRGINIA BEACH BLVD"),
        ("1300 ERNEST BARRETT PKWY STE",     "1300 ERNEST BARRETT PKWY"),
        ("12019 ALDINE WESTFIELD RD STE",    "12019 ALDINE WESTFIELD RD"),
        ("4999 CAROLINA FOREST BLVD UNIT",   "4999 CAROLINA FOREST BLVD"),
        ("12665 VETERANS MEMORIAL DR SUITE", "12665 VETERANS MEMORIAL DR"),
    ]
    for address, expected in incompletes:
       assert pext.return_max_address(pext.seq, address) == expected.upper(), "Imcomplete address {} was not trimmed".format(address)
