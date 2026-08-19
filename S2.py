import sys

from utils.data_structs import DataContainer
from utils.tree_analysis import get_basic_deprel

"""
ID: S2
Inventory question: Which positions of an adverbial clause relative to its governing clause are attested?
UD-oriented version: Which linear orders are attested between a token whose DEPREL is advcl and its governor?
Output - a frequency list of: ADVCL-GOVERNOR; GOVERNOR-ADVCL
"""

input_path = sys.argv[1]
output_path = sys.argv[2]

data_cont = DataContainer("S2", input_path)

for sent in data_cont.parsed_conllu_sents:
    for tok in sent:
        # ignore MW tokens
        if type(tok["id"]) is not int:
            continue

        if get_basic_deprel(tok["deprel"]) == "advcl":
            if tok["id"] < tok["head"]:
                result = "ADVCL-GOVERNOR"
            elif tok["id"] > tok["head"]:
                result = "GOVERNOR-ADVCL"

            data_cont.add_to_results(result, 1, sent.metadata["sent_id"])

data_cont.export_json(output_path, "no_tokens_with_deprel=advcl")