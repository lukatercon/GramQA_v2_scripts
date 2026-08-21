import sys

from utils.data_structs import DataContainer
from utils.tree_analysis import get_basic_deprel

"""
ID: C8
Inventory question: Which word classes can serve as predicates in copular clauses?
UD-oriented version: Which distinct UPOS values are attested on heads that govern a token whose DEPREL is cop?
Output - a frequency list of: UPOS values of copular predicate heads
"""

input_path = sys.argv[1]
output_path = sys.argv[2]

data_cont = DataContainer("C8", input_path)

for sent in data_cont.parsed_conllu_sents:
    for tok in sent:
        # ignore MW tokens
        if type(tok["id"]) is not int:
            continue

        if get_basic_deprel(tok["deprel"]) == "cop":
            data_cont.add_to_results(sent[tok["head"] - 1]["upos"], 1, sent.metadata["sent_id"])

data_cont.export_json(output_path, "no_tokens_with_deprel=cop")