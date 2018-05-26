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
