import sys

from utils.data_structs import DataContainer
from utils.tree_analysis import get_basic_deprel

"""
ID: S1
Inventory question: Which types of subordinate clause are attested?
UD-oriented version: Which distinct DEPREL values from {advcl, ccomp, xcomp, csubj, acl} are attested on subordinate clause heads?
Output - a frequency list of: advcl; ccomp; xcomp; csubj; acl
"""

input_path = sys.argv[1]
output_path = sys.argv[2]

data_cont = DataContainer("S1", input_path)

for sent in data_cont.parsed_conllu_sents:
    for tok in sent:
        # ignore MW tokens
        if type(tok["id"]) is not int:
            continue

        if get_basic_deprel(tok["deprel"]) in ["advcl", "ccomp", "xcomp", "csubj", "acl"]:            
            data_cont.add_to_results(get_basic_deprel(tok["deprel"]), 1, sent.metadata["sent_id"])

data_cont.export_json(output_path, "no_tokens_with_deprel=advcl,ccomp,xcomp,csubj,acl")