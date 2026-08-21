import sys

from utils.data_structs import DataContainer
from utils.tree_analysis import get_basic_deprel

"""
ID: S3
Inventory question: Which subordinate clause types occur with and without an overt subordinating marker?
UD-oriented version: Which combinations of subordinate-clause DEPREL in {advcl, ccomp, xcomp, csubj, acl} and mark-dependent status are attested?
Output - a frequency list of: Relation + marked status, such as advcl+marked or ccomp+unmarked
"""

input_path = sys.argv[1]
output_path = sys.argv[2]

data_cont = DataContainer("S3", input_path)

for sent in data_cont.parsed_conllu_sents:
    for tok in sent:
        # ignore MW tokens
        if type(tok["id"]) is not int:
            continue

        if get_basic_deprel(tok["deprel"]) in ["advcl", "ccomp", "xcomp", "csubj", "acl"]:
            if any([get_basic_deprel(dep["deprel"]) == "mark" and dep["head"] == tok["id"] for dep in sent]):
                result = f"{get_basic_deprel(tok["deprel"])}+marked"
            else:
                result = f"{get_basic_deprel(tok["deprel"])}+unmarked"

            data_cont.add_to_results(result, 1, sent.metadata["sent_id"])

data_cont.export_json(output_path, "no_tokens_with_deprel=advcl,ccomp,xcomp,csubj,acl")