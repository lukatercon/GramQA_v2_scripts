import configparser

from stark.stark import run as stark_run
from stark.stark import read_configs as stark_read_configs

def build_stark_config(settings_dict):
    config = configparser.ConfigParser()
    config["settings"] = settings_dict

    return config


def get_stark_results(stark_config):
    return stark_run(stark_read_configs(stark_config))
