import sys

from utils.data_structs import DataContainer
from utils.tree_analysis import get_basic_deprel

"""
ID: P4
Inventory question: Which orders of noun and numeral are attested?
UD-oriented version: Which linear orders are attested between tokens whose DEPREL is nummod and their heads with UPOS=NOUN?
Output - a frequency list of: numeral before noun; noun before numeral
"""

input_path = sys.argv[1]
output_path = sys.argv[2]

data_cont = DataContainer("P4", input_path)

for sent in data_cont.parsed_conllu_sents:
    for tok in sent:
        # ignore MW tokens and tokens without features
        if type(tok["id"]) is not int:
            continue

        head_id = tok["head"]
        if get_basic_deprel(tok["deprel"]) == "nummod" and sent[head_id - 1]["upos"] == "NOUN":
            if tok["id"] < head_id:
                order = "numeral before noun"
            elif tok["id"] > head_id:
                order = "noun before numeral"

            data_cont.add_to_results(order, 1, sent.metadata["sent_id"])

data_cont.export_json(output_path, "no_tokens_with_deprel=nummod_and_heads_with_UPOS=NOUN")