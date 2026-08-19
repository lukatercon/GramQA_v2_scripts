import sys

from utils.data_structs import DataContainer
from utils.tree_analysis import get_basic_deprel

"""
ID: C10
Inventory question: Which orders of copula and predicate are attested?
UD-oriented version: Which linear orders are attested between a token whose DEPREL is cop and its predicate head?
Output - a frequency list of: COP-PREDICATE; PREDICATE-COP
"""

input_path = sys.argv[1]
output_path = sys.argv[2]

data_cont = DataContainer("C10", input_path)

for sent in data_cont.parsed_conllu_sents:
    for tok in sent:
        # ignore MW tokens
        if type(tok["id"]) is not int:
            continue

        if get_basic_deprel(tok["deprel"]) == "cop":
            if tok["id"] < tok["head"]:
                result = "COP-PREDICATE"
            elif tok["id"] > tok["head"]:
                result = "PREDICATE-COP"

            data_cont.add_to_results(result, 1, sent.metadata["sent_id"])

data_cont.export_json(output_path, "no_tokens_with_deprel=cop")