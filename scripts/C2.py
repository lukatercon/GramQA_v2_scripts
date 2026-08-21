import sys

from utils.data_structs import DataContainer
from utils.tree_analysis import get_basic_deprel

"""
ID: C2
Inventory question: Which orders of subject and verb are attested in intransitive clauses?
UD-oriented version: Which linear orders are attested between tokens with UPOS=VERB and one dependent whose DEPREL is nsubj when the verb has no obj dependent?
Output - a frequency list of: SV; VS
"""

input_path = sys.argv[1]
output_path = sys.argv[2]

data_cont = DataContainer("C2", input_path)

for sent in data_cont.parsed_conllu_sents:
    for tok in sent:
        # ignore MW tokens
        if type(tok["id"]) is not int:
            continue

        subjs = [get_basic_deprel(x["deprel"]) == "nsubj" and x["head"] == tok["id"] for x in sent]
        objs = [get_basic_deprel(y["deprel"]) == "obj" and y["head"] == tok["id"] for y in sent]
        if tok["upos"] == "VERB" and list(filter(bool, subjs)) == [True] and not any(objs):

            dependents = ""
            for dep in sent:
                if dep["id"] == tok["id"]:
                    dependents += "V"

                # skip nsubj:outer subjects, since they are not really linked to the inner verb
                elif dep["head"] == tok["id"] and dep["deprel"]  == "nsubj:outer":
                    continue

                elif dep["head"] == tok["id"] and get_basic_deprel(dep["deprel"])  == "nsubj":
                    dependents += "S"

            data_cont.add_to_results(dependents, 1, sent.metadata["sent_id"])

data_cont.export_json(output_path, "no_tokens_with_UPOS=VERB_and_dependent_with_upos=nsubj_and_no_dependent_with_upos=obj")