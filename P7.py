import sys

from utils.data_structs import DataContainer
from utils.tree_analysis import get_basic_deprel

"""
ID: P7
Inventory question: Which orders of adposition and nominal head are attested?
UD-oriented version: Which linear orders are attested between an UPOS=ADP token whose DEPREL is case and its nominal head with UPOS in {NOUN, PROPN, PRON}?
Output - a frequency list of: ADP-NOMINAL; NOMINAL-ADP
"""

input_path = sys.argv[1]
output_path = sys.argv[2]

data_cont = DataContainer("P7", input_path)

for sent in data_cont.parsed_conllu_sents:
    for tok in sent:
        # ignore MW tokens and tokens without features
        if type(tok["id"]) is not int:
            continue

        head_id = tok["head"]
        if tok["upos"] == "ADP" and get_basic_deprel(tok["deprel"]) == "case" and sent[head_id - 1]["upos"] in ["NOUN", "PROPN", "PRON"]:
            if tok["id"] < head_id:
                order = "ADP-NOMINAL"
            elif tok["id"] > head_id:
                order = "NOMINAL-ADP"

            data_cont.add_to_results(order, 1, sent.metadata["sent_id"])

data_cont.export_json(output_path, "no_tokens_with_UPOS=ADP_and_deprel=case_and_heads_with_UPOS=NOUN,PROPN,PRON")