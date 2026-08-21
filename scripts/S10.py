import sys

from utils.data_structs import DataContainer
from utils.tree_analysis import get_basic_deprel, get_max_tree_depth, is_projective

"""
ID: S10
Inventory question: Which grammatical relations participate in non-projective dependencies?
UD-oriented version: Which distinct DEPREL values are attested on non-projective dependency arcs?
Output - a frequency list of: Main DEPREL labels on non-projective arcs
"""

input_path = sys.argv[1]
output_path = sys.argv[2]

data_cont = DataContainer("S10", input_path)

for sent in data_cont.parsed_conllu_sents:
    for tok in sent:
        # ignore MW tokens
        if type(tok["id"]) is not int:
            continue

        if not is_projective(sent, tok["id"]):
            data_cont.add_to_results(get_basic_deprel(tok["deprel"]), 1, sent.metadata["sent_id"])
    
data_cont.export_json(output_path, "no_non-projective_tokens")
