# Iterate through a list of addresses and collect unique patterns.
import sys
import os
import re

import addrext
import hydraseq

sequencer = addrext.Sequencer()
collector = hydraseq.Hydraseq('_0')

base_path = 'addrext/data/known_good/'
with open('uniques.csv', 'w') as target:
    for fname in ['eighty_k_good_street_and_po_samples.csv', 'full_clean_addresses.csv', 'known_pobox.csv']:
        with open(base_path+fname, 'r') as source:
            for line in source:
                encoding = sequencer.encode_from_word_list(line.lower().split())
                compact = " ".join([word for lst in encoding for word in lst])
                collector.insert(compact+" _0")
                if collector.surprise:
                    target.write("{},{}\n".format( line.lower().strip(), str(encoding)))

print("Unique count: ", len(collector.columns['_0']))

