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
        assert pext.return_max_address3(pext.seq, address) == address.upper(), address

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


def test_shortlist():
    shortlist = [
        ("1 HILLCREST CENTER DRIVE ST 225",    "1 HILLCREST CENTER DRIVE ST 225", "Don't drop the ST"),
        ("8690 SIERRA COLLEGE BLVD STE",       "8690 SIERRA COLLEGE BLVD",        "Drop the extra STE"),
        ("1590 WALLISVILLE ROAD POBOX 10190",  "1590 WALLISVILLE ROAD",           "Should drop the po box"),
        ("1905 N CENTER POINT RD",             "1905 N CENTER POINT RD",          "Do not drop the DR"),
        ("200 W CENTER PROMENADE #500",        "200 W CENTER PROMENADE #500",     "Do not drop PROMENADE"),
    ]
    for address, expected, note in shortlist:
       assert pext.return_max_address3(pext.seq, address) == expected.upper(), note

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
       assert pext.return_max_address3(pext.seq, address) == expected.upper(), "Imcomplete address {} was not trimmed".format(address)


def test_is_suite():
    suites = [
        "suite 255",
    ]

    for suite in suites:
        assert pext.is_suite(pext.seq, suite.lower()) == True, "'{}' should be a suite".format(suite.upper())

    not_suites = [
        "st 255"
        "st"
    ]
    for suite in not_suites:
        assert pext.is_suite(pext.seq, suite.lower()) == False, "'{}' should *NOT* be a suite".format(suite.upper())
