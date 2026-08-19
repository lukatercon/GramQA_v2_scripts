import sys

from utils.data_structs import DataContainer

"""
ID: L8
Inventory question: Which determiners are attested?
UD-oriented version: Which distinct LEMMA values are attested on tokens with UPOS=DET?
Output - a frequency list of: Determiner lemmas
"""

input_path = sys.argv[1]
output_path = sys.argv[2]

data_cont = DataContainer("L8", input_path)

if data_cont.treebank_has_lemmas():
    field_to_check = "lemma"
else:
    field_to_check = "form"

for sent in data_cont.parsed_conllu_sents:
    for tok in sent:
        # ignore MW tokens and tokens that don't have UPOS assigned
        if type(tok["id"]) is not int or tok["upos"] == "_":
            continue

        if tok["upos"] == "DET":
            data_cont.add_to_results(tok[field_to_check], 1, sent.metadata["sent_id"])

data_cont.export_json(output_path, "no_tokens_with_UPOS=DET")
