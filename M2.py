import sys

from utils.data_structs import DataContainer

"""
ID: M2
Inventory question: Which grammatical genders are attested on nouns?
UD-oriented version: Which distinct Gender values are attested on tokens with UPOS=NOUN?
Output - a frequency list of: Gender values on nouns
"""

input_path = sys.argv[1]
output_path = sys.argv[2]

data_cont = DataContainer("M2", input_path)

for sent in data_cont.parsed_conllu_sents:
    for tok in sent:
        # ignore MW tokens and tokens that don't have UPOS or feats assigned
        if type(tok["id"]) is not int or tok["upos"] == "_" or not tok["feats"]:
            continue

        if tok["upos"] == "NOUN" and tok["feats"].get("Gender"):
            data_cont.add_to_results(tok["feats"]["Gender"], 1, sent.metadata["sent_id"])

data_cont.export_json(output_path, "no_tokens_with_UPOS=NOUN_and_Gender_feature")
