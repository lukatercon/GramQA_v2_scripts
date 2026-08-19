import sys

from utils.data_structs import DataContainer

"""
ID: M5
Inventory question: Which verb forms are attested?
UD-oriented version: Which distinct VerbForm values are attested?
Output - a frequency list of: Attested VerbForm values
"""

input_path = sys.argv[1]
output_path = sys.argv[2]

data_cont = DataContainer("M5", input_path)

for sent in data_cont.parsed_conllu_sents:
    for tok in sent:
        # ignore MW tokens and tokens that don't have feats assigned
        if type(tok["id"]) is not int or not tok["feats"]:
            continue

        if tok["feats"].get("VerbForm"):
            data_cont.add_to_results(tok["feats"]["VerbForm"], 1, sent.metadata["sent_id"])

data_cont.export_json(output_path, "no_tokens_with_VerbForm_feature")
