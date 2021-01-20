import pandas as pd
import numpy as np
import json
import configargparse



if __name__ == '__main__':

    p = configargparse.ArgParser(default_config_files=['../config/config.ini'])
    p.add('-mc', '--my-config', is_config_file=True, help='alternative config file path')

    p.add("-oj", "--path_to_original_json_folder", required=False, help="path to original json", type=str)
    p.add("-ej", "--path_to_entities_json_folder", required=False, help="path to entities json", type=str)
    p.add("-pathcsv", "--path_to_csv", required=False, help="path to final csv", type=str)
    p.add("-pathmeta", "--path_to_metadata", required=False, help="path to metadata", type=str)
    p.add("-pathchebi", "--path_chebi", required=False, help="path to metadata", type=str)
    p.add("-pathdo", "--path_do", required=False, help="path to metadata", type=str)
    p.add("-pathgo", "--path_go", required=False, help="path to metadata", type=str)
    p.add("-pathhp", "--path_hp", required=False, help="path to metadata", type=str)

    options = p.parse_args()

    original_json_folder = options.path_to_original_json_folder
    entities_json_folder = options.path_to_entities_json_folder
    path_to_meta = options.path_to_metadata
    path_to_final_csv = options.path_to_csv

    path_chebi = options.path_chebi
    path_do = options.path_do
    path_go = options.path_go
    path_hp = options.path_hp

    rec_sys_data = pd.read_csv(path_to_final_csv, names=['user', 'item', 'rating'])

    result = rec_sys_data.to_json('/data/rec_sys_platform/user_item_rating.json', orient="records", indent=4)

    # parsed = json.loads(result)
    # print(parsed)
    # with open('/data/rec_sys_platform/user_item_rating.json', 'w') as outfile:
    #     json.dumps(parsed, indent=4, sort_keys=True)

