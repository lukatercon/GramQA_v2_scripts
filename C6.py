import sys

from utils.data_structs import DataContainer
from utils.tree_analysis import get_basic_deprel

"""
ID: C6
Inventory question: Which combinations of core arguments are attested with verbs?
UD-oriented version: Which distinct sets of nsubj, csubj, obj, iobj, ccomp and xcomp dependents are attested on tokens with UPOS=VERB?
Output - a frequency list of: none; singleton relation sets; all attested combinations of nsubj, csubj, obj, iobj, ccomp and xcomp
"""

input_path = sys.argv[1]
output_path = sys.argv[2]

data_cont = DataContainer("C6", input_path)

for sent in data_cont.parsed_conllu_sents:
    for tok in sent:
        # ignore MW tokens
        if type(tok["id"]) is not int:
            continue

        if tok["upos"] == "VERB":
            dependents = ""
            for dep in sent:
                if dep["id"] == tok["id"]:
                    dependents += "-VERB-"
                elif dep["head"] == tok["id"] and dep["deprel"] in ["nsubj", "csubj", "obj", "iobj", "ccomp", "xcomp"]:
                    dependents += f"-{dep['deprel']}-"

            dependents = dependents.strip("-")
            if dependents == "HEAD":
                dependents = "none"

            data_cont.add_to_results(dependents, 1, sent.metadata["sent_id"])

data_cont.export_json(output_path, "no_tokens_with_UPOS=VERB")