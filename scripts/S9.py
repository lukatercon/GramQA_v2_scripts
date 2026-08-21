import sys

from utils.data_structs import DataContainer
from utils.tree_analysis import get_basic_deprel, get_max_tree_depth, get_root_level_deprel

"""
ID: S9
Inventory question: How many clauses can sentences contain?
UD-oriented version: Which sentence-level clause-counts are attested?
Output - a frequency list of: 1 clause; 2 clauses; 3 clauses; 4 or more clauses
"""

input_path = sys.argv[1]
output_path = sys.argv[2]

data_cont = DataContainer("S9", input_path)
clause_deprels = ["advcl", "ccomp", "xcomp", "csubj", "acl", "conj", "parataxis", "root"]

for sent in data_cont.parsed_conllu_sents:
    clause_count = 0

    for tok in sent:
        if get_basic_deprel(tok["deprel"]) in clause_deprels:
            clause_count += 1

    match clause_count:
        case 1:
            result = "1 clause"
        case 2:
            result = "2 clauses"
        case 3:
            result = "3 clauses"
        case _:
            result = "4 or more clauses"

    data_cont.add_to_results(result, 1, sent.metadata["sent_id"])

data_cont.export_json(output_path, "no_relevant_sentences")
