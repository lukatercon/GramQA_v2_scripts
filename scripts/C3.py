import sys

from utils.data_structs import DataContainer
from utils.tree_analysis import get_basic_deprel

"""
ID: C3
Inventory question: Which orders of verb and direct object are attested?
UD-oriented version: Which linear orders are attested between tokens with UPOS=VERB and one dependent whose DEPREL is obj?
Output - a frequency list of: VO; OV
"""

input_path = sys.argv[1]
output_path = sys.argv[2]

data_cont = DataContainer("C3", input_path)

for sent in data_cont.parsed_conllu_sents:
    for tok in sent:
        # ignore MW tokens
        if type(tok["id"]) is not int:
            continue

        objs = [get_basic_deprel(y["deprel"]) == "obj" and y["head"] == tok["id"] for y in sent]
        if tok["upos"] == "VERB" and list(filter(bool, objs)) == [True]:

            dependents = ""
            for dep in sent:
                if dep["id"] == tok["id"]:
                    dependents += "V"

                elif dep["head"] == tok["id"] and get_basic_deprel(dep["deprel"])  == "obj":
                    dependents += "O"

            data_cont.add_to_results(dependents, 1, sent.metadata["sent_id"])

data_cont.export_json(output_path, "no_tokens_with_UPOS=VERB_and_dependent_with_upos=obj")