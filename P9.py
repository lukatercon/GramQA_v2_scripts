import sys

from utils.data_structs import DataContainer
from utils.tree_analysis import get_basic_deprel

"""
ID: P9
Inventory question: Which combinations of word classes are attested in coordination?
UD-oriented version: Which unordered pairs of UPOS values are attested between a token whose DEPREL is conj and its head?
Output - a frequency list of: Unordered UPOS pairs linked by conj
"""

input_path = sys.argv[1]
output_path = sys.argv[2]

data_cont = DataContainer("P9", input_path)

for sent in data_cont.parsed_conllu_sents:
    for tok in sent:
        # ignore MW tokens and tokens without features
        if type(tok["id"]) is not int:
            continue

        head_id = tok["head"]
        if get_basic_deprel(tok["deprel"]) == "conj":
            # sort the pair to obtain an arbitrary ordering that will always be the same for the same two items 
            # regardless of which one is the head and which one the dependent
            upos_pair = sorted([tok["upos"], sent[head_id - 1]["upos"]])

            data_cont.add_to_results(str(upos_pair), 1, sent.metadata["sent_id"])

data_cont.export_json(output_path, "no_tokens_with_deprel=conj")