import json
import os
import sys
import time
import xml.etree.ElementTree as ET
from Bio import Entrez

sys.path.append("./")


def output_article_to_json(doc_id, eng_title, eng_abstract, lang, version, lang_title, lang_abstract, authors):
    """Generates two distinct json files including title and abstract from considered article.

    Requires:
        doc_id: is str
        eng_title: is stri
        eng_abstract: is str
        lang: is str, represents 2nd language: 'pt' (Portuguese) or 'spa' (Spanish)
        version: is str, 
        lang_title: is str
        lang_abstract: is str
        authors: is list with info (name, institution) about article authors 

    Ensures:
        two json files (<doc_id>_eng.json and <doc_id>_<lang>.json) in 'abstracts' dir with format:
        {"paper_id": "...",
         "metadata_id": {
            "title": "..."
            "authors": [
                {"first": "...",
                "last": "...",
                "affiliation": {"institution": "...",}]},
         "abstract": [
            {"text": "...",
             "section": "Abstract"
            }
            ]
        }
    """
    eng_doc_id = doc_id + "_en"
    eng_dict = {"paper_id": eng_doc_id, 
                "metadata": {"title":eng_title, "authors": authors}, 
                "abstract": [{"text": eng_abstract, "section": "Abstract"}]}
    eng_out_dict = json.dumps(eng_dict)
    #print(doc_id, "\n", eng_title, "\n", eng_abstract, "\n",  lang, "\n",  lang_title, "\n",  lang_abstract)
    with open("../abstracts_" + version + "/en+" + lang + "/en/" + eng_doc_id + ".json", "w") as eng_out_file:
            eng_out_file.write(eng_out_dict)
            eng_out_file.close()

    lang_doc_id = doc_id + "_" + lang
    lang_dict = {"paper_id": lang_doc_id, 
                "metadata": {"title":lang_title, "authors": authors}, 
                "abstract": [{"text": lang_abstract, "section": "Abstract"}]}
    lang_out_dict = json.dumps(lang_dict)
    
    with open("../abstracts_" + version + "/en+" + lang + "/" + lang + "/" + lang_doc_id + ".json", "w") as lang_out_file:
            lang_out_file.write(lang_out_dict)
            lang_out_file.close()

def retrieve_pubmed_abstracts(lang, version):
    """ Get PubMed abstracts with two multilingual versions (English+lang) using Bio.Entrez package  
        (see: https://biopython.org/docs/1.75/api/Bio.Entrez.html)

    Requires:
        lang: is str, chosen 2nd language, with value "pt" (Portuguese) or "spa" (Spanish)
        version: is str, specifies the documents to include in the dataset, has value "covid_19" 
                (articles striclty related with COVID-19) or "large" (articles indirectly related 
                with COVID-19 (e.g. pulmonary infections, virus, etc.)
    Ensures:
        Retrieve abstracts simultaneously available in English and in selected <lang> and output them in 'abstracts' dir
    """

    Entrez.email = "pedrosimruas@gmail.com" 

    if lang == "pt":

        if version == "covid_19":
            handle = Entrez.esearch(db="pubmed", retmax=1000, term="covid-19 AND English [LANG] AND Portuguese [LANG]")
        
        elif version == "large":
            handle = Entrez.esearch(db="pubmed", retmax=3197, term="2019 Novel Coronavirus Disease OR 2019 Novel Coronavirus   \
                Infection OR 2019-nCoV Disease OR 2019-nCoV Infection OR COVID-19 Pandemic OR COVID-19 Pandemics OR COVID-19  \
                Virus Disease OR COVID-19 Virus OR Infection OR COVID19 OR Coronavirus Disease 2019 OR Coronavirus Disease-19 \
                OR SARS Coronavirus 2 Infection OR SARS-CoV-2 Infection AND English [LANG] AND Portuguese [LANG]") 

    elif lang == "spa":

        if version == "covid_19":
            handle = Entrez.esearch(db="pubmed", retmax=1000, term="covid-19 AND English [LANG] AND Spanish [LANG]")
        
        elif version == "large":
            handle = Entrez.esearch(db="pubmed", retmax=5071, term="2019 Novel Coronavirus Disease OR 2019 Novel Coronavirus   \
                Infection OR 2019-nCoV Disease OR 2019-nCoV Infection OR COVID-19 Pandemic OR COVID-19 Pandemics OR COVID-19  \
                Virus Disease OR COVID-19 Virus OR Infection OR COVID19 OR Coronavirus Disease 2019 OR Coronavirus Disease-19 \
                OR SARS Coronavirus 2 Infection OR SARS-CoV-2 Infection AND English [LANG] AND Spanish [LANG]")

    record = Entrez.read(handle)
    handle.close() 

    doc_count, abstract_count = int(), int()
    total_retrieved_doc = len(record['IdList'])

    for doc_id in record['IdList']: # Iterate over each retrieved document
        doc_count += 1
        print(doc_count, "/", total_retrieved_doc)
        doc_handle = Entrez.efetch(db="pubmed", id=doc_id, retmode="xml")# Retrieve document information
        doc_record = Entrez.read(doc_handle)
        doc_handle.close()
        
        article = doc_record['PubmedArticle'][0]['MedlineCitation']
        eng_abstract = str()
            
        if 'Abstract' in article['Article'].keys(): # Some documents have no english abstract
            eng_content = article['Article']['Abstract']
        
        authors = list()
        
        if 'AuthorList' in article['Article'].keys():# Get authors info: only consider articles with at least 1 author
            
            for author in article['Article']['AuthorList' ]: 
                
                if 'ForeName' in author.keys() and 'LastName' in author.keys(): #Some authors are collective, e.g. 'ColectiveAuthor'
                    author_dict = {"first": author['ForeName'], "last": author['LastName'], 
                                    "affiliation": ""}
                    
                    if len(author['AffiliationInfo']) >= 1: #Some authors do not have affiliation info
                        if 'Affiliation' in author['AffiliationInfo'][0].keys():
                            author_dict["affiliation"] = author['AffiliationInfo'][0]['Affiliation']
                
                    authors.append(author_dict) 
            
            eng_title = article['Article']['ArticleTitle']
            article_langs = article['Article']['Language']
        
            # Check if the article has english and portuguese/spanish abstracts
            if article['OtherAbstract'] != [] and eng_content["AbstractText"] != None and len(article_langs) == 2: 
                lang_title = str()

                if 'VernacularTitle' in doc_record['PubmedArticle'][0]['MedlineCitation']['Article'].keys():
                    lang_title = doc_record['PubmedArticle'][0]['MedlineCitation']['Article']['VernacularTitle']

                lang_content = article['OtherAbstract'][0]['AbstractText']
                lang_abstract, eng_abstract = str(), str()

                for element in lang_content:
                    lang_abstract += element
                    
                for element in eng_content['AbstractText']:
                    eng_abstract += element
                
                output_article_to_json(doc_id, eng_title, eng_abstract, lang, version, lang_title, lang_abstract, authors)
                abstract_count += 1
    
    print("Retrieved docs: ", str(doc_count), "\nDocs with en +", \
        str(lang), "abstracts available: ", str(abstract_count), \
        "(", str((abstract_count/doc_count)*100), "% )")


if __name__ == "__main__":
    start_time = time.time()
    
    lang = sys.argv[1] # "pt" (Portuguese) or "spa" (Spanish)
    version = sys.argv[2] # "covid_19" (articles striclty related with COVID-19 or 
                          # "large" (articles indirectly related with COVID-19 (e.g. pulmonary infections, virus, etc.))
    
    output_dir = "../abstracts_" + version + "/en+" + str(lang) + "/"

    if not os.path.exists(output_dir + "en"):
        os.makedirs(output_dir + "en")

    if not os.path.exists(output_dir + str(lang)):
        os.makedirs(output_dir + str(lang))

    retrieve_pubmed_abstracts(lang, version)
    
    end_time = time.time()
    total_min= round((end_time-start_time)/60, 2)
    print("Total time:", str(total_min), "min")




