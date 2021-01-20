import unidecode

def get_user_item_rating(list_of_authors, df_entities):

    user_item_rating = []

    for author in list_of_authors:
        for entity in df_entities.entities_id:
            user_item_rating.append([author, entity, 1])


    return user_item_rating



def remove_accents(a):
    return unidecode.unidecode(a.decode('utf-8'))



def remove_accents_from_authors(records_df, column):
    records_df[column] = records_df[column].astype('unicode')
    records_df[column] =  records_df[column].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

    # for i in range(records_df[column].size):
    #
    #     for b in range(len(records_df[column][i])):
    #         records_df[column][i][b] = unidecode.unidecode(records_df[column][i][b])

    return records_df