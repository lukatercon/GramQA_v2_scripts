import sys

from utils.data_structs import DataContainer

"""
ID: L6
Inventory question: Which words function as coordinating markers?
UD-oriented version: Which distinct LEMMA values are attested on tokens whose DEPREL is cc?
Output - a frequency list of: Coordinating-marker lemmas
"""

input_path = sys.argv[1]
output_path = sys.argv[2]

data_cont = DataContainer("L6", input_path)

if data_cont.treebank_has_lemmas():
    field_to_check = "lemma"
else:
    field_to_check = "form"

for sent in data_cont.parsed_conllu_sents:
    for tok in sent:
        # ignore MW tokens and tokens that don't have deprel assigned
        if type(tok["id"]) is not int or tok["deprel"] == "_":
            continue

        if tok["deprel"].split(":")[0] == "cc":
            data_cont.add_to_results(tok[field_to_check], 1, sent.metadata["sent_id"])

data_cont.export_json(output_path, "no_tokens_with_deprel=cc")
