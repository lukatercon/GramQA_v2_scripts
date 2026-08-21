import sys

from utils.data_structs import DataContainer
from utils.tree_analysis import get_basic_deprel, get_max_tree_depth, get_root_level_deprel

"""
ID: S7
Inventory question: Which grammatical roles can occur in sentence-initial position?
UD-oriented version: Which DEPREL values are attested on the root-level constituent whose subtree contains the first non-punctuation token?
Output - a frequency list of: Root-level relations such as nsubj, obj, obl, advcl and root
"""

input_path = sys.argv[1]
output_path = sys.argv[2]

data_cont = DataContainer("S7", input_path)

for sent in data_cont.parsed_conllu_sents:
    # find the first non-punctuation token ID in sentence
    first_tok_id = 1
    while sent[first_tok_id - 1]["upos"] == "PUNCT":
        first_tok_id += 1
        if first_tok_id > len(sent):
            first_tok_id = None
            break

    # skip sentences with only punctuation tokens
    if not first_tok_id:
        continue

    result = get_root_level_deprel(sent, first_tok_id)
    data_cont.add_to_results(result, 1, sent.metadata["sent_id"])

data_cont.export_json(output_path, "no_sentences_with_non-punctuation_tokens")
