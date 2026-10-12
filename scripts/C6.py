import sys
import re

from utils.data_structs import DataContainer
from utils.tree_analysis import get_basic_deprel
from utils.stark_extraction import build_stark_config, get_stark_results

"""
ID: C6
Inventory question: Which combinations of core arguments are attested with verbs?
UD-oriented version: Which distinct sets of nsubj, csubj, obj, iobj, ccomp and xcomp dependents are attested on tokens with UPOS=VERB?
Output - a frequency list of: none; singleton relation sets; all attested combinations of nsubj, csubj, obj, iobj, ccomp and xcomp
"""

input_path = sys.argv[1]
output_path = sys.argv[2]

data_cont = DataContainer("C6", input_path, do_parse=False)

# P8 and C6 are implemented using calls to the STARK library
stark_config = build_stark_config({
    "input": input_path,
    "labeled": "yes",
    "label_subtypes": "no",
    "fixed": "yes",
    "size": "2-1000",
    "head": "upos=VERB",
    "ignored_labels": "flat|cop|root|punct|det|advcl|dep|cc|clf|expl|discourse|fixed|conj|dislocated|nmod|advmod|appos|orphan|goeswith|list|case|vocative|obl|aux|acl|amod|parataxis|reparandum|nummod|mark|compound",
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
        data_cont.add_to_results(re.sub(r"\(.*\)", "_", tree[0]), int(tree[1]), "", tree[6])  # the regex substitution makes sure the trees only go one layer deep
            
data_cont.export_json(output_path, "no_tokens_with_UPOS=VERB_with_relevant_dependents")
