import sys

from utils.data_structs import DataContainer
from utils.tree_analysis import get_basic_deprel

"""
ID: C7
Inventory question: Which grammatical cases are attested on direct objects?
UD-oriented version: Which distinct Case values are attested on tokens whose DEPREL is obj?
Output - a frequency list of: Case values on direct objects
"""

input_path = sys.argv[1]
output_path = sys.argv[2]

data_cont = DataContainer("C7", input_path)

for sent in data_cont.parsed_conllu_sents:
    for tok in sent:
        # ignore MW tokens
        if type(tok["id"]) is not int or not tok["feats"]:
            continue

        if get_basic_deprel(tok["deprel"]) == "obj" and tok["feats"].get("Case"):
            data_cont.add_to_results(tok["feats"]["Case"], 1, sent.metadata["sent_id"])

data_cont.export_json(output_path, "no_tokens_with_deprel=obj_and_Case_feature")