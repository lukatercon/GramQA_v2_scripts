from tqdm import tqdm

import subprocess
import os
import logging
from collections import defaultdict

treebanks_dir = os.path.join("ud-treebanks-v2.18")
scripts_dir = os.path.join("..", "scripts")
output_dir = os.path.join("output")

if not os.path.isdir(os.path.join(output_dir, "log")):
    os.mkdir(os.path.join(output_dir, "log"))

logging.basicConfig(filename=os.path.join(output_dir, "log", "run_on_ud_2-18.log"), level=logging.INFO)
logger = logging.getLogger(__name__)

na_dict = defaultdict(list)

for script in tqdm(os.listdir(scripts_dir), desc="Progress through scripts"):
    if not os.path.isfile(os.path.join(scripts_dir, script)) or not script.endswith(".py"):
        continue

    script_path = os.path.join(scripts_dir, script)

    for treebank in os.listdir(treebanks_dir):
        if not os.path.isdir(os.path.join(output_dir, treebank)):
            os.mkdir(os.path.join(output_dir, treebank))
            
        for file in os.listdir(os.path.join(treebanks_dir, treebank)):
            if file.endswith("2.18.conllu"):
                input_file_path = os.path.join(treebanks_dir, treebank, file)

                output_file_path = os.path.join(output_dir, treebank, script.split(".py")[0] + "_results.json")

                try:
                    subprocess.run(["python", script_path, input_file_path, output_file_path], 
                                   check=True, capture_output=True, text=True)
                except subprocess.CalledProcessError as e:
                    logger.error(f"Error while running {script} with {treebank}: {e.stderr}\n\n\n")
                else:
                    with open(output_file_path, "r", encoding="utf-8") as rf_output:
                        if '"status": "N/A",' in rf_output.read():
                            na_dict[script].append(treebank)

logger.info("\nScripts returned N/A in the following cases:\n")
logger.info("\n".join([f"{k}: No. of langs with N/A: {len(v)}. Langs list: {v}" for k, v in na_dict.items()]))
