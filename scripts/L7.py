import sys

from utils.data_structs import DataContainer
from utils.tree_analysis import get_token_subtree

"""
ID: L7
Inventory question: Which subordinating markers are attested?
UD-oriented version: Which distinct LEMMA values are attested on tokens whose DEPREL is mark?
Output - a frequency list of: Marker lemmas
"""

input_path = sys.argv[1]
output_path = sys.argv[2]

data_cont = DataContainer("L7", input_path)

if data_cont.treebank_has_lemmas():
    field_to_check = "lemma"
else:
    field_to_check = "form"

for sent in data_cont.parsed_conllu_sents:
    for tok in sent:
        # ignore MW tokens and tokens that don't have deprel assigned
        if type(tok["id"]) is not int or tok["deprel"] == "_":
            continue

        if tok["deprel"].split(":")[0] == "mark":
            data_cont.add_to_results(get_token_subtree(sent, tok["id"], field_to_check),
                                     1, sent.metadata["sent_id"])

data_cont.export_json(output_path, "no_tokens_with_deprel=mark")
