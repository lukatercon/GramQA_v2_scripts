import sys

from utils.data_structs import DataContainer
from utils.tree_analysis import get_basic_deprel

"""
ID: C5
Inventory question: Which word classes can function as subjects?
UD-oriented version: Which distinct UPOS values are attested on tokens whose DEPREL is nsubj?
Output - a frequency list of: UPOS values of nominal subjects
"""

input_path = sys.argv[1]
output_path = sys.argv[2]

data_cont = DataContainer("C5", input_path)

for sent in data_cont.parsed_conllu_sents:
    for tok in sent:
        # ignore MW tokens
        if type(tok["id"]) is not int:
            continue

        if get_basic_deprel(tok["deprel"]) == "nsubj":
            data_cont.add_to_results(tok["upos"], 1, sent.metadata["sent_id"])

data_cont.export_json(output_path, "no_tokens_with_deprel=nsubj")