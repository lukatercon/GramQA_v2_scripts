import sys

from utils.data_structs import DataContainer
from utils.tree_analysis import get_basic_deprel

"""
ID: S4
Inventory question: Which positions of a subordinating marker relative to its clause head are attested?
UD-oriented version: Which linear orders are attested between a token whose DEPREL is mark and its subordinate predicate head?
Output - a frequency list of: MARKER-CLAUSE_HEAD; CLAUSE_HEAD-MARKER
"""

input_path = sys.argv[1]
output_path = sys.argv[2]

data_cont = DataContainer("S4", input_path)

for sent in data_cont.parsed_conllu_sents:
    for tok in sent:
        # ignore MW tokens
        if type(tok["id"]) is not int:
            continue

        if get_basic_deprel(tok["deprel"]) == "mark":
            if tok["id"] < tok["head"]:
                result = f"MARKER-CLAUSE_HEAD"
            elif tok["id"] > tok["head"]:
                result = f"CLAUSE_HEAD-MARKER"

            data_cont.add_to_results(result, 1, sent.metadata["sent_id"])

data_cont.export_json(output_path, "no_tokens_with_deprel=mark")
