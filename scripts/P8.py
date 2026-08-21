import sys

from utils.data_structs import DataContainer
from utils.tree_analysis import get_basic_deprel
from utils.stark_extraction import build_stark_config, get_stark_results

"""
ID: P8
Inventory question: Which basic noun phrase structures are attested?
UD-oriented version: Which distinct sets of det, clf, amod, nummod, nmod, appos and acl dependents, including no such dependents, are attested on tokens with UPOS=NOUN?
Output - a frequency list of: none; singleton relation sets; all attested combinations of det, clf, amod, nummod, nmod, appos and acl
"""

input_path = sys.argv[1]
output_path = sys.argv[2]

data_cont = DataContainer("P8", input_path, do_parse=False)

# P8 and C6 are implemented using calls to the STARK library
stark_config = build_stark_config({
    "input": input_path,
    "labeled": "yes",
    "label_subtypes": "no",
    "fixed": "yes",
    "size": "2-1000",
    "head": "upos=NOUN",
    "allowed_labels": "det|clf|amod|nummod|nmod|appos|acl",
    "association_measures": "yes",
    "example": "yes",
    "grew_match": "no",
    "depsearch": "no",
    "node_info": "no",
    "head_info": "yes",
    "greedy_counter": "yes",
    "complete": "yes"
})

results = get_stark_results(stark_config)

if len(results) > 1:
    for tree in results[1:]:
        data_cont.add_to_results(tree[0], int(tree[1]), "", tree[6])
            
data_cont.export_json(output_path, "no_tokens_with_UPOS=NOUN")