import conllu
import os
import json


class DataContainer:
    def __init__(self, q_id, filepath):
        # parsed conllu file
        self.parsed_conllu_sents = self.parse_conllu(filepath)

        # question ID
        self.item_id = q_id

        # get info from filepath
        self.lang, self.treebank, self.ud_release = self.parse_filepath(filepath)
        self.treebank = "UD_" + self.treebank

        # answer status - initialized as None, can be either "OK" or "N/A"
        self.status = None

        # total - sum of all item counts in the result table
        self.total = 0

        # the result table - a dictionary with a key (item name corresponding to one of the allowed result item types) and a list value 
        # consisting of the frequency of the item in question and an example sentence ID. 
        # When exporting to json, each item should be rendered as {"key": "...", "count": 0, "example_sent_id": "..."}
        self.table = dict()

        # N/A reason - only if the status is N/A. Initialized as None, then changes to a string detailing a question-specific reason for the N/A status
        self.na_reason = None  


    # parse conllu file and return parsed sentence list with MW tokens removed
    def parse_conllu(self, filepath):
        with open(filepath, "r", encoding="utf-8") as rf:
            conllu_sents = conllu.parse(rf.read())

        # discard MW tokens
        clean_sents = list()
        for orig_sent in conllu_sents:
            clean_sents.append(orig_sent.filter(id=lambda x: type(x) is int))

        return clean_sents


    # parse various info from the filename .
    # the scripts expect filenames in the form: "sl_Slovenian-SSJ_2.18.conllu", which stands for lang-code_treebank-name_UD-version.conllu
    # the treebank name is the name of the github repository without the initial "UD_"
    def parse_filepath(self, filepath):
        lang_code, treebank_name, ud_version = ".".join(os.path.split(filepath)[-1].split(".")[:-1]).split("_")

        return lang_code, treebank_name, ud_version


    # method for adding an item to the result table.
    # In the actual scripts, this can be called on the level of an individual word (where the cound should only be incremented by one) or a whole sentence, 
    # where all occurrences of the item are added at once if several occurrences are found in the same sentence.
    def add_to_results(self, key_name, count, sent_id):
        assert count > 0, "The count passed to the add_to_results function should be a nonzero positive integer."

        if key_name not in self.table.keys():
            self.table[key_name] = [count, sent_id]
        else:
            self.table[key_name][0] += count

        self.total += count


    # method for exporting a json-formatted file - called at the end of each script
    def export_json(self, outpath, na_reason_str):
        # first add the status
        if len(self.table) > 0:
            self.status = "OK"
        else:
            self.status = "N/A"

        # build the JSON object
        json_obj = {
            "item_id": self.item_id,
            "lang": self.lang,
            "treebank": self.treebank,
            "ud_release": self.ud_release,
            "status": self.status,
            "total": self.total,
            "table": [
                {"key": k, "count": v[0], "example_sent_id": v[1]} for k, v in self.table.items()
            ]
        }  

        # add the na reason if applicable
        if self.status == "N/A":
            self.na_reason = na_reason_str
            json_obj["na_reason"] = self.na_reason

        # export to file
        with open(outpath, "w", encoding="utf-8") as wf:
            wf.write(json.dumps(json_obj, indent=4))


    # method for checking if a treebank has lemmas at all - in cases where lemmas are missing (if such cases indeed occur), the current
    # solution is to search for word forms instead
    def treebank_has_lemmas(self):
        for sent in self.parsed_conllu_sents:
            for tok in sent:
                if tok["lemma"] != "_":
                    return True

        return False
