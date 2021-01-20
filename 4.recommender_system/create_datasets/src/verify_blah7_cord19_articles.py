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



def upload_relations(path_to_relations):

    df = pd.read_csv(path_to_relations, sep='\t', skiprows=[0], names=['entity_1', 'entity_2', 'relation'])

    return df


def map_relations(df):

    rel_label = ['effect', 'no_relation']
    rel_numeric = [1, 0]

    df_rel = pd.DataFrame(rel_label, columns=["label"])
    df_rel['num'] = rel_numeric

    df["relation_numeric"] = df["relation"].map(df_rel.set_index('label')["num"]).fillna(0)


    return df




def verify_articles_overlapping(cord_dir, blah_dir):
    list_of_articles_cord = list_files_in_directory(cord_dir)
    list_of_articles_blah = list_files_in_directory(blah_dir)

    user_item_rating_all = []

    list_of_cord_titles = []
    list_of_cord_ids = []
    list_of_bla_titles = []
    list_of_bla_ids = []

    print("CORD-19")
    for file in list_of_articles_cord:
        file = file.strip('.json')
        j_file = open_json_file(cord_dir, file)
        title = get_article_title(j_file)
        title = unidecode.unidecode(title)
        list_of_cord_titles.append(title)
        list_of_cord_ids.append(get_id(j_file))

    print('BLAH')
    for file in list_of_articles_blah:
        file = file.split('.')[0]
        j_file = open_json_file(blah_dir, file)
        title = get_article_title(j_file)
        list_of_bla_ids.append(get_id(j_file))
        title = unidecode.unidecode(title)
        list_of_bla_titles.append(title)

    df = pd.DataFrame(np.array(list_of_cord_titles), columns=['cord_titles'])
    df['cord_ids'] = np.array(list_of_cord_ids)

    blah_in_df = df[df.cord_titles.isin(list_of_bla_titles)]

    df_blah = pd.DataFrame(np.array(list_of_bla_titles), columns=['blah_titles'])
    df_blah['blah_ids'] = np.array(list_of_bla_ids)

    print(blah_in_df)



def verify_entities(relations_file, rec_sys_file):

    '''
    verify how namy entities are shared between the entities in the relation and
    in the rec sys dataset
    :param relations_file:
    :param rec_sys_file:
    :return:
    '''

    df_relations = upload_relations(relations_file)

    #df_relations = map_relations(df_relations)

    rec_sys_data = pd.read_csv(rec_sys_file, sep=",", names=['user', 'item', 'rating'])

    all_entities_relations_unique = np.unique(np.concatenate((df_relations.entity_1, df_relations.entity_2), axis=0))

    df_all_entities_relations_unique = pd.DataFrame(all_entities_relations_unique, columns=['entity'])
    rec_sys_entities_unique = np.unique(rec_sys_data.item)



    print('entities in relations: ', all_entities_relations_unique.shape)
    print('entities in rec sys: ', rec_sys_entities_unique.shape)
    print('shared entities: ', df_all_entities_relations_unique[df_all_entities_relations_unique.entity.isin(rec_sys_entities_unique.tolist())].shape)
    print(df_all_entities_relations_unique[df_all_entities_relations_unique.entity.isin(rec_sys_entities_unique.tolist())])



if __name__ == '__main__':

    cord_dir = '/data/covid_data/2020-03-13/comm_use_subset/comm_use_subset/'
    blah_dir = '/data/blah7/abstracts_large/en+pt/en/'

    relations_file = '/data/covid_data/RE/results/joint_results_identifiers.tsv'

    rec_sys_file = '/data/blah7/rec_sys_datasets/blah7_abstracts_large_recsys_dataset_user_item_rating_enpt.csv'



    verify_articles_overlapping(cord_dir, blah_dir)

    verify_entities(relations_file, rec_sys_file)









