import sys
sys.path.append("../")
import addrext
safety = 10
sequencer = addrext.Sequencer()

print("Address, Sentence,sequence,max_branch,markers,all_branches,keepers")
with open('contents.csv', 'r') as source:
    for line in source:
        # if safety <= 0:
        #     break
        # else:
        #     safety -= 1
        sub_lines = [sub_line for sub_line in line.strip().replace('"',"'").split('.') if len(sub_line.strip()) > 0]
        for sub_line in sub_lines:
            expected, max_branch, markers, all_branches, keepers = sequencer.convert_high_address_validate_transform(sub_line, {}, allthree=True)
            print('"',expected, '","', sub_line, '","',sequencer.encode_from_word_list(sequencer.tokenize_to_list(expected.lower())) , '","', max_branch, '","', markers,'","', all_branches, '","',keepers, '"')
