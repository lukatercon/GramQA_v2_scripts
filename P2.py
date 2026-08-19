import sys

from utils.data_structs import DataContainer
from utils.tree_analysis import get_basic_deprel

"""
ID: P2
Inventory question: Which orders of noun and demonstrative are attested?
UD-oriented version: Which linear orders are attested between tokens with PronType=Dem whose DEPREL is det and their heads with UPOS=NOUN?
Output - a frequency list of: demonstrative before noun; noun before demonstrative
"""

input_path = sys.argv[1]
output_path = sys.argv[2]

data_cont = DataContainer("P2", input_path)

for sent in data_cont.parsed_conllu_sents:
    for tok in sent:
        # ignore MW tokens and tokens without features
        if type(tok["id"]) is not int or not tok["feats"]:
            continue

        head_id = tok["head"]
        if tok["feats"].get("PronType") == "Dem" and get_basic_deprel(tok["deprel"]) == "det" and sent[head_id - 1]["upos"] == "NOUN":
            if tok["id"] < head_id:
                order = "demonstrative before noun"
            elif tok["id"] > head_id:
                order = "noun before demonstrative"

            data_cont.add_to_results(order, 1, sent.metadata["sent_id"])

data_cont.export_json(output_path, "no_tokens_with_PronType=Dem_and_deprel=det_and_heads_with_UPOS=NOUN")