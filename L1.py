import sys

from utils.data_structs import DataContainer

"""
ID: L1
Inventory question: Which word classes are attested?
UD-oriented version: Which distinct UPOS values are attested among non-punctuation syntactic words in the UD data?
Output - a frequency list of: UPOS values, excluding PUNCT

usage example: python L1.py treebank_file.conllu output_file.json
"""

input_path = sys.argv[1]
output_path = sys.argv[2]

data_cont = DataContainer("L1", input_path)

for sent in data_cont.parsed_conllu_sents:
    for tok in sent:
        # ignore MW tokens, punctuation, and tokens that don't have an UPOS assigned
        if type(tok["id"]) is not int or tok["upos"] in ["PUNCT", "_"]:
            continue

        data_cont.add_to_results(tok["upos"], 1, sent.metadata["sent_id"])

data_cont.export_json(output_path, "no_non-punctuation_UPOS_tags")
