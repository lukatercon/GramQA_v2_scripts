import sys

from utils.data_structs import DataContainer
from utils.tree_analysis import get_basic_deprel

"""
ID: P10
Inventory question: Which word classes can be modified by an adverb?
UD-oriented version: Which distinct head UPOS values are attested for UPOS=ADV dependents whose DEPREL is advmod?
Output - a frequency list of: Head UPOS values of adverbial modifiers
"""

input_path = sys.argv[1]
output_path = sys.argv[2]

data_cont = DataContainer("P10", input_path)

for sent in data_cont.parsed_conllu_sents:
    for tok in sent:
        # ignore MW tokens and tokens without features
        if type(tok["id"]) is not int:
            continue

        head_id = tok["head"]
        if tok["upos"] == "ADV" and get_basic_deprel(tok["deprel"]) == "advmod":

            data_cont.add_to_results(sent[head_id - 1]["upos"], 1, sent.metadata["sent_id"])

data_cont.export_json(output_path, "no_tokens_with_UPOS=ADV_and_deprel=adv")