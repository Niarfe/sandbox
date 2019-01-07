import csv
import os
import pytest
import sys
sys.path.append(".")
os.chdir("{}/../".format(os.path.dirname(os.path.realpath(__file__))))

#import field_validate_transform_address as sequencer
from addrext import Sequencer
sequencer = Sequencer()

def test_markers():
    marker_lengths = [
        ("123 main st", 2),
        ("901 s bolmar st # a", 2),
    ]
    for address, length in marker_lengths:
        assert len(sequencer.get_markers(address, ['_ADDRESS_'])) == length, "{} should have {} markers".format(address, length)

def test_basics():
    valid_addresses = [
        "123 MAIN ST",
        "901 S BOLMAR ST # A",
        "300 PHOENIX MILLS PLZ"
    ]

    for address in valid_addresses:
        assert sequencer.convert_high_address_validate_transform(address) == address.lower(), address

# def test_pobox():
#     sent = "po box 7001"
#     assert sequencer.is_pobox(sequencer.seq, sequencer.tokenize_to_list(sent)) == True

# def test_attn():
#     sent = "attn john doe"
#     assert sequencer.is_deleg(sequencer.seq, sequencer.tokenize_to_list(sent)) == True


def test_multiple_markers():
    marker_lengths = [
        ("123 main st", 2),
        ("901 s bolmar st # a", 2),
        ("123 main st c/o gustav mahler", 4)
    ]
    for address, length in marker_lengths:
        assert len(sequencer.get_markers(address, ['_ADDRESS_', '_ATTN_'])) == length, "{} should have {} markers".format(address, length)


def test_shortlist():
    shortlist = [
        ("100 CAPITOLA DRIVE STD 275","100 CAPITOLA DRIVE STD 275",""),
        ("4189 nunc road lebanon", "4189 nunc road", "do not confuse city with address"),
        ("po box 456 123 main st", "123 main st", "do not pick up from pobox"),
        ("123 main po box 456", "123 main", "choose address over pobox"),
        ("535 W GYPSY LN RD LOT 330","535 W GYPSY LN RD LOT 330","drops suite"),
        ("21W487 TANAGER COURT","21W487 TANAGER COURT","drops it all"),
        ("759 HWY ZZ","759 HWY ZZ","It dropped all of it"),
        ("350 G STREET #E-1","350 G STREET #E-1","drops suite"),
        ("5093 S WHITAKER DRIVE 2310-W","5093 S WHITAKER DRIVE 2310-W","drops suite 2310-w"),
        ("2606 BOIS D'ARC LANE","2606 BOIS D'ARC LANE","Drops lane"),
        ("20 CHURCH ST APT #2","20 CHURCH ST APT #2", "dropped apt with #2"),
        ("N 7940 HWY E","N 7940 HWY E","didn't even get partial crediat"),
        ("1700 J STREET APT #707","1700 J STREET APT #707","Drops that apt"),
        ("300 9TH ST NORTHEAST","300 9TH ST NORTHEAST","Doesn't see last DIR"),
        ("102 WEST NORTH BOX 278","102 WEST NORTH","it kept the wrong side!"),
        ("1377 E FLORENCE BLVD #151-103","1377 E FLORENCE BLVD #151-103","Dropped suites"),
        ("117 SOUTH 13TH ST 1ST FLOOR APT 1","117 SOUTH 13TH ST 1ST FLOOR APT 1","drops apt 1"),
        ("10237 RED LION TAVERN","10237 RED LION TAVERN","Drops Tavern"),
        ("1206 AVE L","1206 AVE L","Drops the whole thing"),
        ("4 TROWBRIDGE PL #PH", "4 TROWBRIDGE PL #PH", "Drops the #PH"),
        ("601 1/2 BELVUE STREET","601 1/2 BELVUE STREET","drops STREET"),
        ("192 SOUTH UNION RD APT #4","192 SOUTH UNION RD APT #4","Drops apt, literaly, like apt, but not #4"),
        ("25075 525 ST","25075 525 ST","IT NUKES IT COMPLETELY, WHY?"),
        ("1 HILLCREST CENTER DRIVE ST 225",    "1 HILLCREST CENTER DRIVE ST 225", "Don't drop the ST"),
        ("8690 SIERRA COLLEGE BLVD STE",       "8690 SIERRA COLLEGE BLVD",        "Drop the extra STE"),
        ("1590 WALLISVILLE ROAD POBOX 10190",  "1590 WALLISVILLE ROAD",           "Should drop the po box"),
        ("1905 N CENTER POINT RD",             "1905 N CENTER POINT RD",          "Do not drop the DR"),
        ("200 W CENTER PROMENADE #500",        "200 W CENTER PROMENADE #500",     "Do not drop PROMENADE"),
        ("ZERO DUVAL STREET",                  "ZERO DUVAL STREET",               "ZERO is a valid street number?"),
        ("THIRTY-ONE NEW CHARDON STREET",      "THIRTY-ONE NEW CHARDON STREET",   "THIRTY-ONE is a valid street number"),
        ("PO BOX RKM",                         "PO BOX RKM",                      "PO BOXes can have alpha ids"),
        ("PO BOX QQ",                          "PO BOX QQ",                       "PO BOXes can have alpha ids"),
        ("PO BOX C-847",                       "PO BOX C-847",                    "PO BOXes can have mixed alpha num symbol ids"),
        ("N72W13536 Lund Lane Apt 116",        "N72W13536 Lund Lane Apt 116",     ""),
        ("1072 ST. CLAIR ROAD",                "1072 ST CLAIR ROAD",              ""),
        ("880 GOR-AN FARM RD",                 "880 GOR-AN FARM RD",              ""),
        ("2602 E. SAN JOSE APT 9",             "2602 E SAN JOSE APT 9",    ""),
        ("65A BIRD OF PARADISE DR",            "65A BIRD OF PARADISE DR",  ""),
        ("4876 Co Rd 650",                     "4876 Co Rd 650",           ""),
        ("1070 WAYATT GROVE CHURCH ROAD","1070 WAYATT GROVE CHURCH ROAD",""),
        ("291 B PARK RIDGE LN","291 B PARK RIDGE LN",""),
        ("13130 FRY RD NO 1625","13130 FRY RD NO 1625",""),
        ("1444 CO RD X","1444 CO RD X",""),
        ("1200 ST HWY 184","1200 ST HWY 184",""),
        ("2545 N83RD AVENUE NO.1151",           "2545 N83RD AVENUE NO 1151",""),
        ("APT 10 270 WEBERS LANE",              "APT 10 270 WEBERS LANE",""),
        ("8645 D GOLD PEAK PL","8645 D GOLD PEAK PL",""),
        ("9116 D SW 20TH COURT","9116 D SW 20TH COURT",""),
        ("7706 SANTA LUCIA COURT","7706 SANTA LUCIA COURT",""),
        ("33 W DELAWARE PLACE APT 21 J","33 W DELAWARE PLACE APT 21 J","This is only catching the 21 and J as separate suites"),
        ("5657 KY HIGHWAY 154","5657 KY HIGHWAY 154",""),
        ("231 26TH AVENUE EAST NO 211","231 26TH AVENUE EAST NO 211",""),
        ("507 1/2 WEST FAWN STREET","507 1/2 WEST FAWN STREET",""),
        ("PO Bxo 428","PO Bxo 428",""),
        ("11023 ST ANTHONYS COURT","11023 ST ANTHONYS COURT",""),
        ("9643 ST RT 65","9643 ST RT 65",""),
        ("19 SAN EUGENIO","19 SAN EUGENIO",""),
        ("2522 D S ARLINGTON MILL DR","2522 D S ARLINGTON MILL DR",""),
        ("432 PONCE DE LEON DRIVE","432 PONCE DE LEON DRIVE",""),
        ("201 KENT AVE NO 3","201 KENT AVE NO 3",""),
        ("1432 - 58TH STREET","1432 - 58TH STREET",""),
        ("21846 J.D.ADAMS DRIVE","21846 J D ADAMS DRIVE",""),
        ("1803 Haight Ave Number 3F","1803 Haight Ave Number 3F",""),
        ("85 - 3RD STREET","85 - 3RD STREET",""),
        ("9147 San Diego Road","9147 San Diego Road",""),
        ("701 LUPO LANE APT E23 HUNTERS RUN","701 LUPO LANE APT E23",""),
        ("57835-148TH ST","57835-148TH ST",""),
        ("3695 Santa Rosa Way","3695 Santa Rosa Way",""),
        ("APARTMENT 43 1625 BRADFIELD DRIVE","APARTMENT 43 1625 BRADFIELD DRIVE",""),
        ("5502 D Shadow Glen CT","5502 D Shadow Glen CT",""),
        ("17101 CO RD 263","17101 CO RD 263",""),
        ("349 CO. RD. 396","349 CO RD 396",""),
        ("101 MONTGOMERY AVENUE APT. B-1","101 MONTGOMERY AVENUE APT B-1",""),
        ("3020 W. SAN JUAN DRIVE","3020 W SAN JUAN DRIVE",""),
        ("PO BOX 5041IG BEAVER","PO BOX 5041IG",""),
        ("PO BOX 3277-CRS","PO BOX 3277-CRS",""),
        ("A-5717 138TH AVE","A-5717 138TH AVE",""),
        ("966-C PARK STREET","966-C PARK STREET",""),
        ("936-C OLD CLEMSON HIGHWAY","936-C OLD CLEMSON HIGHWAY",""),
        ("901-C CLINT MOORE ROAD","901-C CLINT MOORE ROAD",""),
        ("9005-C RED BRANCH RD","9005-C RED BRANCH RD",""),
        ("724-4TH STREET","724-4TH STREET",""),
        ("6541-C FRANZ WARNER PARKWAY","6541-C FRANZ WARNER PARKWAY",""),
        ("5901-A PEACHTREE DUNWOODY RD","5901-A PEACHTREE DUNWOODY RD",""),
        ("5000-14TH AVENUE","5000-14TH AVENUE",""),
        ("4215-D STUART ANDREW BLVD","4215-D STUART ANDREW BLVD",""),
        ("3903-A FAIR RIDGE DR","3903-A FAIR RIDGE DR",""),
        ("3421-M SAIN VARDELL LANE","3421-M SAIN VARDELL LANE",""),
        ("3110-A ASHFORD DUNWOODY RD","3110-A ASHFORD DUNWOODY RD",""),
        ("2929-A CAPITAL MEDICAL BLVD","2929-A CAPITAL MEDICAL BLVD",""),
        ("2500NW 39TH STREET","2500NW 39TH STREET",""),
        ("21-A OAK BRANCH DRIVE","21-A OAK BRANCH DRIVE",""),
        ("20001-A EMERALD COAST PARKWAY","20001-A EMERALD COAST PARKWAY",""),
        ("199-A FAIRBURN INDUSTRIAL BLVD","199-A FAIRBURN INDUSTRIAL BLVD",""),
        ("142-A TALATHA CHURCH ROAD","142-A TALATHA CHURCH ROAD",""),
        ("1301-A LEMAIRE","1301-A LEMAIRE",""),
        ("108-A PARK PLACE COURT","108-A PARK PLACE COURT",""),
        ("100-B FORSYTH HALL DRIVE","100-B FORSYTH HALL DRIVE",""),
        ("NOTTINGHAM VILLAGE SQUARE 2653-A WHITEHORSE-HAMILTON SQ","2653-A WHITEHORSE-HAMILTON SQ",""),
        ("9401LITTLE RIVER TPKE","9401LITTLE RIVER TPKE",""),
        ("50THIELMAN DRIVE","50THIELMAN DRIVE",""),
        ("411BUTTERNUT DR", "411BUTTERNUT DR", ""),
        ("1101 W MURRAY DR Rm 607B","1101 W MURRAY DR Rm 607B",""),
        ("15422 40 AVE EAST", "15422 40 AVE EAST", ""),
        ("2871 LOWER EAST VALLEY RD", "2871 LOWER EAST VALLEY RD", ""),
        ("G3371 N CENTER RD", "G3371 N CENTER RD", ""),
        ("811 SAND LOT CIRCLE", "811 SAND LOT CIRCLE", ""),
        ("16318 95TH AVE CT EAST", "16318 95TH AVE CT EAST", ""),
        ("C/O Dell&Schaefer Law Firm    2404 Hollywood Blvd", "2404 Hollywood Blvd", "it botches the c/o part"),
        ("1200 ST HWY 184", "1200 ST HWY 184", "sees 184 as the suite not as the name"),
        ("6754 RD K NE", "6754 RD K NE", ""),
        ("2466 HIGHWAY 17-A SOUTH", "2466 HIGHWAY 17-A SOUTH", ""),
        ("62 COLLINS LANDING D UNIT 63", "62 COLLINS LANDING D UNIT 63", "sees D as suite only"),
        ("33 W DELAWARE PLACE APT 21 J", "33 W DELAWARE PLACE APT 21 J", "its ok on sheet, but sees two suites for 21 and for J"),
        ("PO BOX 506, 89 DOLANS PT PK RD", "89 DOLANS PT PK RD", "almost ok but dropped the PK RD"),
        ("350 N. State Hwy 360 Apt 11205", "350 N State Hwy 360 Apt 11205", "came out ok but taggged two suites"),
        ("75 MCKINELY AVENUE, UNIT B2-2", "75 MCKINELY AVENUE , UNIT B2-2", ""),
        ("151 PARKWAY NORTH APT 302", "151 PARKWAY NORTH APT 302", ""),
        ("4050 W 5 POINT HIGHWAY", "4050 W 5 POINT HIGHWAY", "its ok but took 4050 W to be suite"),
        ("23461 US HWY 5 N No. 818", "23461 US HWY 5 N No 818", "ok but took triple suite"),
        ("1010 SHAGBARK RD 1 C", "1010 SHAGBARK RD 1 C", "ok, but it took C as suite and left the 1 as address..."),
        ("6900 STONERIDGE DR E33", "6900 STONERIDGE DR E33", "how are we supposed to tell that E33 is the suite? not the address?"),
        ("1431 MAPLEWOOD ST N.E.", "1431 MAPLEWOOD ST N.E.", "[[0, 4, 4, ['ADDRESS'], '1431 maplewood st n'], [4, 5, 1, ['_DIR_', 'SUITE'], 'e']]"),
        ("452 Union B Rd.", "452 UNION B RD", "[[0, 2, 2, ['ADDRESS'], '452 union'], [2, 3, 1, ['SUITE'], 'b']]"),
        ("17504 27TH AVE N.E.","17504 27TH AVE N E","[[0, 1, 1, ['SUITE'], '17504'], [1, 5, 4, ['ADDRESS'], '27th ave n e']]"),
    ]
    for address, expected, note in shortlist:
        assert sequencer.convert_high_address_validate_transform(address) == " ".join(sequencer.tokenize_to_list(expected.lower())), sequencer.get_markers(expected.lower(),['_ADDRESS_', '_POBOX_', '_SUITE_', '_DIR_']) #'{},"{}"'.format(expected.lower(), sequencer.encode_from_word_list(sequencer.tokenize_to_list(expected.lower())))

@pytest.mark.xfail
def test_expected_to_fail():
    shortlist = [
          ("3970 REBECK RD East St Paul","3970 REBECK RD","[[0, 4, 4, ['ADDRESS'], '3970 rebeck rd east']]"),
    ]
    for address, expected, note in shortlist:
        assert vtad.convert_high_address_validate_transform(address) == " ".join(vtad.tokenize_to_list(expected.lower())), '{},"{}"'.format(expected.lower(),vtad.encode_from_word_list(vtad.tokenize_to_list(expected.lower())))

# expected to faile because SUITE can be interpreted as SUIT+E which is a misspelling of 'suite e', this is to cover cases like STEC which means 'suite c'
@pytest.mark.xfail
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
       assert sequencer.convert_high_address_validate_transform(address) == expected.lower(), '{},"{}"'.format(address.lower(), sequencer.encode_from_word_list(sequencer.tokenize_to_list(address.lower())))


# def test_is_suite():
#     suites = [
#         "suite 255",
#     ]

#     for suite in suites:
#         assert sequencer.is_suite(sequencer.seq, suite.lower()) == True, "'{}' should be a suite".format(suite.lower())

#     not_suites = [
#         "st 255"
#         "st"
#     ]
#     for suite in not_suites:
#         assert sequencer.is_suite(sequencer.seq, suite.lower()) == False, "'{}' should *NOT* be a suite".format(suite.lower())

