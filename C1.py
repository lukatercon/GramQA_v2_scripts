import sys

from utils.data_structs import DataContainer
from utils.tree_analysis import get_basic_deprel

"""
ID: C1
Inventory question: Which orders of subject, verb and direct object are attested?
UD-oriented version: Which of the six linear orders are attested among tokens with UPOS=VERB, one dependent whose DEPREL is nsubj and one dependent whose DEPREL is obj?
Output - a frequency list of: SVO; SOV; VSO; VOS; OVS; OSV
"""

input_path = sys.argv[1]
output_path = sys.argv[2]

data_cont = DataContainer("C1", input_path)

for sent in data_cont.parsed_conllu_sents:
    for tok in sent:
        # ignore MW tokens
        if type(tok["id"]) is not int:
            continue

        if tok["upos"] == "VERB" and any([get_basic_deprel(x["deprel"]) == "nsubj" and x["head"] == tok["id"] for x in sent]) \
                                     and any([get_basic_deprel(y["deprel"]) == "obj" and y["head"] == tok["id"] for y in sent]):

            dependents = ""
            for dep in sent:
                if dep["id"] == tok["id"]:
                    dependents += "V"

                # skip nsubj:outer subjects, since they are not really linked to the inner verb
                elif dep["head"] == tok["id"] and dep["deprel"]  == "nsubj:outer":
                    continue

                elif dep["head"] == tok["id"] and get_basic_deprel(dep["deprel"])  == "nsubj":
                    dependents += "S"

                elif dep["head"] == tok["id"] and get_basic_deprel(dep["deprel"])  == "obj":
                    dependents += "O"

            data_cont.add_to_results(dependents, 1, sent.metadata["sent_id"])

data_cont.export_json(output_path, "no_tokens_with_UPOS=VERB_and_dependent_with_upos=nsubj_and_upos=obj")