import sys

from utils.data_structs import DataContainer
from utils.tree_analysis import get_basic_deprel

"""
ID: P8
Inventory question: Which basic noun phrase structures are attested?
UD-oriented version: Which distinct sets of det, clf, amod, nummod, nmod, appos and acl dependents, including no such dependents, are attested on tokens with UPOS=NOUN?
Output - a frequency list of: none; singleton relation sets; all attested combinations of det, clf, amod, nummod, nmod, appos and acl
"""

input_path = sys.argv[1]
output_path = sys.argv[2]

data_cont = DataContainer("P8", input_path)

for sent in data_cont.parsed_conllu_sents:
    for tok in sent:
        # ignore MW tokens and tokens without features
        if type(tok["id"]) is not int:
            continue

        if tok["upos"] == "NOUN":
            dependents = ""
            for dep in sent:
                if dep["id"] == tok["id"]:
                    dependents += "-HEAD-"
                elif dep["head"] == tok["id"] and dep["deprel"] in ["det", "clf", "amod", "nummod", "nmod", "appos", "acl"]:
                    dependents += f"-{dep['deprel']}-"

            dependents = dependents.strip("-")
            if dependents == "HEAD":
                dependents = "none"

            data_cont.add_to_results(dependents, 1, sent.metadata["sent_id"])

data_cont.export_json(output_path, "no_tokens_with_UPOS=NOUN")