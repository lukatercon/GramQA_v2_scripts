import sys

from utils.data_structs import DataContainer
from utils.tree_analysis import get_basic_deprel

"""
ID: P1
Inventory question: Which orders of noun and adjective are attested?
UD-oriented version: Which linear orders are attested between tokens whose DEPREL is amod and their heads with UPOS=NOUN?
Output - a frequency list of: adjective before noun; noun before adjective
"""

input_path = sys.argv[1]
output_path = sys.argv[2]

data_cont = DataContainer("P1", input_path)

for sent in data_cont.parsed_conllu_sents:
    for tok in sent:
        # ignore MW tokens
        if type(tok["id"]) is not int:
            continue

        head_id = tok["head"]
        if get_basic_deprel(tok["deprel"]) == "amod" and sent[head_id - 1]["upos"] == "NOUN":
            if tok["id"] < head_id:
                order = "adjective before noun"
            elif tok["id"] > head_id:
                order = "noun before adjective"

            data_cont.add_to_results(order, 1, sent.metadata["sent_id"])

data_cont.export_json(output_path, "no_tokens_with_deprel=amod_and_heads_with_UPOS=NOUN")