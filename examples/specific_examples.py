import addrext

sequencer = addrext.Sequencer()

print("Sentence,Address,max_branch,markers,all_branches,keepers")
with open('examples/data/specific_examples.csv', 'r') as source:
    for line in source:
        expected, max_branch, markers, all_branches, keepers = sequencer.parse(line.lower(), allthree=True)
        print(line.strip(), ',"', expected,'","', max_branch, '","', markers,'","', all_branches, '","',keepers, '"')
