from os import walk
import pandas as pd
import numpy as np
import json
import unidecode

import sys

def list_files_in_directory(path_to_dir):


    f = []
    for (dirpath, dirnames, filenames) in walk(path_to_dir):
        f.extend(filenames)
        break

    return f


def open_json_file_pd(dir_path, filename):

    json_file = pd.read_json(dir_path + filename, orient = 'index')

    return json_file

def open_json_file(folder, file):
    with open(folder + file + '.json', encoding='utf-8') as json_file:

        data = json.load(json_file)


    return data



def get_entities(json_file):

    my_dict = json_file.loc['entities'][0]
    my_df = pd.DataFrame(my_dict.items(), columns=['entities', 'count'])

    return my_df


def get_entities_id(df):

    df['entities_id'] = df.entities.str.split(pat="/").str[-1]

    return df


def get_article_id(j_file):

    article_id = j_file.loc['id'].values[0]

    return article_id

def get_article_title(data):


    title = data['metadata']['title']

    return title


def get_id(data):


    id = data['paper_id']

    return id

def get_authors_names(data):

    list_of_authors = []
    for p in data['metadata']['authors']:
        if len(p['first']) == 0 or len(p['last']) == 0:
           continue

        else:

            first = unidecode.unidecode(p['first'])

            last = unidecode.unidecode(p['last'])

            list_of_authors.append(first + ', '+  last)

    return list_of_authors


