import sys

from utils.data_structs import DataContainer
from utils.tree_analysis import get_basic_deprel, get_max_tree_depth

"""
ID: S5
Inventory question: Which levels of clausal embedding are attested in sentences?
UD-oriented version: Which maximum clausal embedding-depth categories are attested per sentence using relation chains from {advcl, ccomp, xcomp, csubj, acl}?
Output - a frequency list of: 0; 1; 2; 3+ levels
"""

input_path = sys.argv[1]
output_path = sys.argv[2]

data_cont = DataContainer("S5", input_path)

for sent in data_cont.parsed_conllu_sents:
    max_sent_depth = get_max_tree_depth([tok for tok in sent if type(tok["id"]) is int], 
                                        permitted_relations=["advcl", "ccomp", "xcomp", "csubj", "acl"])

    if max_sent_depth < 3:
        result = str(max_sent_depth)
    else:
        result = "3+ levels"

    data_cont.add_to_results(result, 1, sent.metadata["sent_id"])

data_cont.export_json(output_path, "no_relevant_sentences_or_tokens_in_treebank")
