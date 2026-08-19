import sys

from utils.data_structs import DataContainer

"""
ID: M9
Inventory question: Which aspect distinctions are attested on verbal forms?
UD-oriented version: Which distinct Aspect values are attested on tokens with UPOS in {VERB, AUX}?
Output - a frequency list of: Aspect values on VERB and AUX
"""

input_path = sys.argv[1]
output_path = sys.argv[2]

data_cont = DataContainer("M9", input_path)

for sent in data_cont.parsed_conllu_sents:
    for tok in sent:
        # ignore MW tokens and tokens that don't have UPOS or feats assigned
        if type(tok["id"]) is not int or tok["upos"] == "_" or not tok["feats"]:
            continue

        if tok["upos"] in ["VERB", "AUX"] and tok["feats"].get("Aspect"):
            data_cont.add_to_results(tok["feats"]["Aspect"], 1, sent.metadata["sent_id"])

data_cont.export_json(output_path, "no_tokens_with_UPOS=VERB,AUX_and_Aspect_feature")
