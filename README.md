# GramQA_v2_scripts
Gold standard extraction scripts (v2) for the GramQA dataset

## Usage
The environment.yml file contains all required dependencies:
```
conda env create -f environment.yml
```

Each script can be run in the following way (for example for the script covering the question ID L1):
```
python L1.py treebank_file.conllu output_file.json
```

the scripts expect filenames in the form "lang-code_treebank-name_UD-version.conllu". For example, in the case of the 2.15 version of the Slovenian SSJ treebank this will be "sl_Slovenian-SSJ_2.18.conllu".
