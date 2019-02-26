#!/usr/bin/env python3
import sys
def hlight(txt, fg=0, bk=1): print(u"\u001b[{};{};1;{}m{}{}".format(0, fg, bk, txt, u"\u001b[0m"))


try:
    import addrext as ax
    print("Using PIP installed package!")
except:
    sys.path.append('../')
    import addrext as ax

seq = ax.Sequencer()

sent = " ".join(sys.argv[1:]) 

if not sent:
    print("\n\tPlease enter an address or string of words after the script.")
    print("\tFor example:  validate_address.py 234 main st")
    sys.exit(0)

hlight("\nInput: "+sent, fg=32, bk=1)

print("\nLatent Encoding: ", seq.encode_from_word_list(seq.tokenize_to_list(sent.lower())))

print("\nParse:")
for idx, ret in enumerate(seq.parse(sent, allthree=True)):
    if idx == 0:
        hlight("FOUND ADDRESS: "+ret, fg=34, bk=1)
    else:
        print(idx, "   ",ret)
print("\nMARKERS:")
for marker in seq.get_markers(sent, ['_ADDRESS_', '_POBOX_', '_SUITE_', '_DIR_']):
    print(marker)
