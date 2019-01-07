import addrext as ax
seq = ax.Sequencer()

sent = "146 lamp and lantern way"

print(sent)
for ret in seq.convert_high_address_validate_transform(sent, allthree=True):
    print("HIT: ",ret)

print("MARKERS:")
print(seq.get_markers(sent, ['_ADDRESS_', '_POBOX_', '_SUITE_', '_DIR_']))
