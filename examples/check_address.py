import addrext as ax
seq = ax.Sequencer()

sent = input("string: ") 

print(sent)
for ret in seq.parse(sent, allthree=True):
    print("HIT: ",ret)

print("MARKERS:")
print(seq.get_markers(sent, ['_ADDRESS_', '_POBOX_', '_SUITE_', '_DIR_']))
