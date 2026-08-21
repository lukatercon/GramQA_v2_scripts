import sys

from utils.data_structs import DataContainer
from utils.tree_analysis import get_basic_deprel, get_max_tree_depth

"""
ID: S8
Inventory question: Which dependency directions are attested?
UD-oriented version: Are both head-before-dependent and dependent-before-head orders attested among dependency arcs excluding root and punct?
Output - a frequency list of: HEAD-DEPENDENT; DEPENDENT-HEAD
"""

input_path = sys.argv[1]
output_path = sys.argv[2]

data_cont = DataContainer("S8", input_path)

for sent in data_cont.parsed_conllu_sents:
    for tok in sent:
        # ignore MW tokens, root relations and punctuation relations
        if type(tok["id"]) is not int or get_basic_deprel(tok["deprel"]) in ["root", "punct"]:
            continue

        if tok["id"] < tok["head"]:
            result = "DEPENDENT-HEAD"
        elif tok["id"] > tok["head"]:
            result = "HEAD-DEPENDENT"

        data_cont.add_to_results(result, 1, sent.metadata["sent_id"])
    
data_cont.export_json(output_path, "no_non-punctuation_or_non-root_tokens")
