import pandas as pd
import configargparse
from data import *
import sys
import json
from create_rec_sys_dataset import *
import numpy as np
import unidecode
import os
import rdflib
from rdflib import URIRef
import implicit
from scipy.sparse import coo_matrix
import pickle


pd.set_option('display.max_columns', None)
pd.set_option("max_rows", None)


def load_ontology(onto_path):

    g = rdflib.Graph()

    g.load(onto_path)


    return g


def get_labels(list_of_uris, list_ids, chebi, hp, go, do):

    labels = []

    for uri, id in zip(list_of_uris, list_ids):

        if id.startswith('CHEBI'):
            #owlClass = rdflib.namespace.OWL.Class
            #rdfType = rdflib.namespace.RDF.type
            uri =  URIRef(uri)
            lab = chebi.label(uri)
            labels.append(lab)

        elif id.startswith('GO'):
            #owlClass = rdflib.namespace.OWL.Class
            #rdfType = rdflib.namespace.RDF.type
            uri =  URIRef(uri)
            lab = go.label(uri)
            labels.append(lab)

        elif id.startswith('HP'):
            # owlClass = rdflib.namespace.OWL.Class
            # rdfType = rdflib.namespace.RDF.type
            uri = URIRef(uri)
            lab = hp.label(uri)
            labels.append(lab)

        elif id.startswith('DO'):
            # owlClass = rdflib.namespace.OWL.Class
            # rdfType = rdflib.namespace.RDF.type
            uri = URIRef(uri)
            lab = do.label(uri)
            labels.append(lab)


            #print(g.label(uri))

    return labels


def create_papers_json(entities_list_of_json_files, entities_json_folder, original_json_folder ):
    count = 0

    data = []

    for file in entities_list_of_json_files:
        print(count, "-", len(entities_list_of_json_files))

        j_file_entities = open_json_file_pd(entities_json_folder, file)

        df_entities = get_entities_id(get_entities(j_file_entities))

        article_id = get_article_id(j_file_entities)

        j_file_original = open_json_file(original_json_folder, article_id)

        list_of_authors = get_authors_names(j_file_original)

        publish_date = metadata[metadata.sha == article_id].publish_time.values
        title = unidecode.unidecode(metadata[metadata.sha == article_id].title.values[0])

        doi = metadata[metadata.sha == article_id].doi.values

        # entities_labels = get_labels(df_entities.entities, df_entities.entities_id, chebi, hp, go, do)

        # df_entities['labels'] = entities_labels

        paper = {
                'id': article_id,
                'title': title,
                'publish_date': publish_date[0],
                'authors': list_of_authors,
                'entities': df_entities.entities_id.to_list(),
                'doi': doi[0]
        }

        data.append(paper)



        # if count == 10:
        #     print(data)
        #
        #     with open('data_test.txt', 'w') as outfile:
        #         json.dump(data, outfile, indent=4, sort_keys=True)
        #     break
        #
        count += 1

    with open('/data/rec_sys_platform/articles.json', 'w') as outfile:
        json.dump(data, outfile, indent=4, sort_keys=True)


def create_entities_json(list_of_entities, chebi, hp, go, do ):

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

        entity = {

                'id': id,
                'label': lab,
                'uri': uri
        }


        entities.append(entity)

    with open('/data/rec_sys_platform/entities.json', 'w') as outfile:
        json.dump(entities, outfile, indent=4, sort_keys=True)


        # count+=1
        # if count == 10:
        #     print(entities)
        #
        #     with open('entities_test.txt', 'w') as outfile:
        #         json.dump(entities, outfile, indent=4, sort_keys=True)
        #     sys.exit()



def id_to_index(df):
    """
    maps the values to the lowest consecutive values
    :param df: pandas Dataframe with columns user, item, rating
    :return: pandas Dataframe with the columns index_item and index_user
    """


    index_item = np.arange(0, len(df.item.unique()))
    index_user = np.arange(0, len(df.user.unique()))

    df_item_index = pd.DataFrame(df.item.unique(), columns=["item"])
    df_item_index["new_index"] = index_item
    df_user_index = pd.DataFrame(df.user.unique(), columns=["user"])
    df_user_index["new_index"] = index_user

    df["index_item"] = df["item"].map(df_item_index.set_index('item')["new_index"]).fillna(0)
    df["index_user"] = df["user"].map(df_user_index.set_index('user')["new_index"]).fillna(0)
    #print(df)

    return df


def three_columns_matrix_to_csr(matrix):
    '''

    :param matrix: pandas dataframe of user, item, rating
    :return: (item, user) rating sparse matrix
    '''

    print(len(matrix.index_item.unique()), len(matrix.index_user.unique()))

    ratings_sparse = coo_matrix((matrix.rating, (matrix.index_item, matrix.index_user)))
    # print(ratings_train_sparse_CF.toarray().shape)

    return ratings_sparse


def create_implicit_model(df):
    df = id_to_index(df)

    model_als = implicit.als.AlternatingLeastSquares(factors=200, num_threads=20, use_gpu=False)

    ratings_sparse = three_columns_matrix_to_csr(df)

    model_als.fit(ratings_sparse)

    pickle.dump(model_als, open('/data/rec_sys_model/model_als.pkl', 'wb'))

    return


def use_implicit_model(df):
    df = id_to_index(df)


    df_user = df[df.index_user == 10]

    ratings_sparse = three_columns_matrix_to_csr(df_user)

    ratings_sparse = ratings_sparse.T.tocsr()

    loaded_model = pickle.load(open('/data/rec_sys_model/model_als.pkl', 'rb'))

    #item_user_data = np.array([23, 53, 123, 67])


    recommendations = loaded_model.recommend(10, ratings_sparse)

    print(recommendations)



    return


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

    list_of_entities = rec_sys_data.item.unique()
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

    entities_list_of_json_files = list_files_in_directory(entities_json_folder)

    metadata = pd.read_csv(path_to_meta)



    # print(metadata.head())
    create_papers_json(entities_list_of_json_files, entities_json_folder, original_json_folder)

    # print("entrou aqui")
    create_entities_json(list_of_entities, chebi, hp, go, do)

    # create_implicit_model(rec_sys_data)

    #use_implicit_model(rec_sys_data)




















