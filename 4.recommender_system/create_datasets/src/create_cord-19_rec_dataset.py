'''
creates a user, item, rating, user_id, item_label csv file
cord-19 corpus
'''

import pandas as pd
import configargparse
from data import *
import sys
import json
from create_rec_sys_dataset import *
import numpy as np
import unidecode
import rdflib
from rdflib import URIRef



pd.set_option('display.max_columns', None)
pd.set_option("max_rows", None)


def id_to_index(df):
    """
    maps the values to the lowest consecutive values
    :param df: pandas Dataframe with columns user, item, rating
    :return: pandas Dataframe with the columns index_item and index_user
    """

    index_user = np.arange(0, len(df.user.unique()))

    df_user_index = pd.DataFrame(df.user.unique(), columns=["user"])
    df_user_index["new_index"] = index_user

    df["index_user"] = df["user"].map(df_user_index.set_index('user')["new_index"]).fillna(0)
    #print(df)

    return df


def load_ontology(onto_path):

    g = rdflib.Graph()

    g.load(onto_path)


    return g



def get_entities_labels(list_of_entities, chebi, hp, go, do ):

    entities = []
    count = 0

    for id in list_of_entities:

        uri = URIRef('http://purl.obolibrary.org/obo/' + id)

        if id.startswith('CHEBI'):

            lab = chebi.label(uri)

        elif id.startswith('GO'):

            lab = go.label(uri)

        elif id.startswith('HP'):

            lab = hp.label(uri)

        elif id.startswith('DO'):

            lab = do.label(uri)


        entities.append(lab)

    return entities



if __name__ == '__main__':

    p = configargparse.ArgParser(default_config_files=['../config/config.ini'])
    p.add('-mc', '--my-config', is_config_file=True, help='alternative config file path')

    p.add("-oj", "--path_to_original_json_folder", required=False, help="path to original json", type=str)
    p.add("-ej", "--path_to_entities_json_folder", required=False, help="path to entities json", type=str)
    p.add("-pathcsv", "--path_to_csv", required=False, help="path to final csv", type=str)
    p.add("-pathchebi", "--path_chebi", required=False, help="path to metadata", type=str)
    p.add("-pathdo", "--path_do", required=False, help="path to metadata", type=str)
    p.add("-pathgo", "--path_go", required=False, help="path to metadata", type=str)
    p.add("-pathhp", "--path_hp", required=False, help="path to metadata", type=str)

    options = p.parse_args()

    original_json_folder = options.path_to_original_json_folder
    entities_json_folder = options.path_to_entities_json_folder

    path_to_final_csv = options.path_to_csv

    path_chebi = options.path_chebi
    path_do = options.path_do
    path_go = options.path_go
    path_hp = options.path_hp

    entities_list_of_json_files = list_files_in_directory(entities_json_folder)

    user_item_rating_all = []

    count = 0

    for file in entities_list_of_json_files:
        print(count, "-", len(entities_list_of_json_files))


        j_file_entities = open_json_file_pd(entities_json_folder, file)

        df_entities = get_entities_id(get_entities(j_file_entities))

        article_id = get_article_id(j_file_entities)

        j_file_original = open_json_file(original_json_folder, article_id)

        list_of_authors = get_authors_names(j_file_original)

        user_item_rating = get_user_item_rating(list_of_authors, df_entities)

        user_item_rating_all.append(user_item_rating)


        count+=1

    flat_list = []
    for sublist in user_item_rating_all:
        for item in sublist:
            flat_list.append(item)



    array = np.array(flat_list)

    final_data = pd.DataFrame(array,  columns=['user', 'item', 'rating'])

    sum_df = final_data.groupby(['user', 'item']).size().reset_index().rename(columns={0: 'rating'})

    df_with_user_id = id_to_index(sum_df)

    ### get entities labels
    list_of_entities = df_with_user_id.item.unique()
    print(list_of_entities)

    ###load ontos

    chebi = load_ontology(path_chebi)
    print("chebi")
    do = load_ontology(path_do)
    print('do')
    go = load_ontology(path_go)
    print('go')
    hp = load_ontology(path_hp)
    print('hp')




    df_user_id = df_with_user_id[['index_user', 'item', 'rating']]

    df_user_name = df_with_user_id[['index_user', 'item', 'rating']]

    entities_label = get_entities_labels(list_of_entities, chebi, hp, go, do)
    print(entities_label)

    df_entities = pd.DataFrame(list_of_entities, columns=["item_id"])
    df_entities["entity_name"] = np.array(entities_label)

    print('mapping labels')
    df_with_user_id["item_name"] = df_with_user_id["item"].map(df_entities.set_index('item_id')["entity_name"]).fillna(0)
    # print(df)

    print('saving')
    df_with_user_id.to_csv(path_to_final_csv, index=False, header=False)














