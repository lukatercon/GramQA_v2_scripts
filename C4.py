import sys

from utils.data_structs import DataContainer
from utils.tree_analysis import get_basic_deprel

"""
ID: C4
Inventory question: How is the subject of a finite clause expressed: as a nominal, as a clause or left unexpressed?
UD-oriented version: Which subject-relation profiles are attested on finite verbal clause heads: nsubj, csubj, both or neither?
Output - a frequency list of: Nominal subject; clausal subject; both; no overt subject relation
"""

input_path = sys.argv[1]
output_path = sys.argv[2]

data_cont = DataContainer("C4", input_path)

for sent in data_cont.parsed_conllu_sents:
    for tok in sent:
        # ignore MW tokens
        if type(tok["id"]) is not int or not tok["feats"]:
            continue

        if tok["upos"] == "VERB" and tok["feats"].get("VerbForm") == "Fin":
            dependents = set()
            for dep in sent:
                # skip nsubj:outer subjects, since they are not really linked to the inner verb
                if dep["head"] == tok["id"] and dep["deprel"]  == "nsubj:outer":
                    continue

                if dep["head"] == tok["id"] and get_basic_deprel(dep["deprel"]) in ["nsubj", "csubj"]:
                    dependents.add(get_basic_deprel(dep["deprel"]))

            if dependents == {"nsubj", "csubj"}:
                result = "both"
            elif dependents == {"nsubj"}:
                result = "nominal subject"
            elif dependents == {"csubj"}:
                result = "clausal subject"
            else:
                result = "no overt subject relation"

            data_cont.add_to_results(result, 1, sent.metadata["sent_id"])

data_cont.export_json(output_path, "no_tokens_with_UPOS=VERB_and_VerbForm=Fin")