import sys

from utils.data_structs import DataContainer

"""
ID: M4
Inventory question: Which gender distinctions are attested on third-person personal pronouns?
UD-oriented version: Which distinct Gender values are attested on tokens with UPOS=PRON, PronType=Prs and Person=3?
Output - a frequency list of: Gender values on third-person personal pronouns
"""

input_path = sys.argv[1]
output_path = sys.argv[2]

data_cont = DataContainer("M4", input_path)

for sent in data_cont.parsed_conllu_sents:
    for tok in sent:
        # ignore MW tokens and tokens that don't have UPOS or feats assigned
        if type(tok["id"]) is not int or tok["upos"] == "_" or not tok["feats"]:
            continue

        if tok["upos"] == "PRON" and tok["feats"].get("PronType") == "Prs" and tok["feats"].get("Person") == "3" and tok["feats"].get("Gender"):
            data_cont.add_to_results(tok["feats"]["Gender"], 1, sent.metadata["sent_id"])

data_cont.export_json(output_path, "no_tokens_with_UPOS=PRON_and_PronType=Prs_and_Person=3_and_Gender_feature")
