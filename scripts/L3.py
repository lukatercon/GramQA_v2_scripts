import sys

from utils.data_structs import DataContainer

"""
ID: L3
Inventory question: Which words function as copulas?
UD-oriented version: Which distinct LEMMA values are attested on tokens whose DEPREL is cop?
Output - a frequency list of: Copula lemmas
"""

input_path = sys.argv[1]
output_path = sys.argv[2]

data_cont = DataContainer("L3", input_path)

if data_cont.treebank_has_lemmas():
    field_to_check = "lemma"
else:
    field_to_check = "form"

for sent in data_cont.parsed_conllu_sents:
    for tok in sent:
        # ignore MW tokens and tokens that don't have a deprel assigned
        if type(tok["id"]) is not int or tok["deprel"] in ["_"]:
            continue

        if tok["deprel"].split(":")[0] == "cop":
            data_cont.add_to_results(tok[field_to_check], 1, sent.metadata["sent_id"])

data_cont.export_json(output_path, "no_cop_dependency_relations")
