import sys

from utils.data_structs import DataContainer
from utils.tree_analysis import get_fixed_expressions

"""
ID: L9
Inventory question: Which fixed expressions are attested?
UD-oriented version: Which ordered LEMMA sequences are attested in connected structures whose internal DEPREL is fixed?
Output - a frequency list of: Ordered lemma sequences of fixed components
"""

input_path = sys.argv[1]
output_path = sys.argv[2]

data_cont = DataContainer("L9", input_path)

if data_cont.treebank_has_lemmas():
    field_to_check = "lemma"
else:
    field_to_check = "form"

for sent in data_cont.parsed_conllu_sents:
    # call the helper function while ignoring MW tokens
    all_fixed = get_fixed_expressions([tok for tok in sent if type(tok["id"]) is int], field_to_check)

    for f_e in all_fixed:
        data_cont.add_to_results(f_e, 1, sent.metadata["sent_id"])

data_cont.export_json(output_path, "no_tokens_with_deprel=fixed")
