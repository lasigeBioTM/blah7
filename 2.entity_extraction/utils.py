import csv
import obonet
import os
import sys

sys.path.append("./")


def load_ctd_vocabularies(vocabulary):
    """Loads MEDIC, CTD-Chemicals, or CTD-Anatomy vocabulary into name_to_id dict  """

    print("Loading", vocabulary)

    name_to_id = dict()

    with open(vocabulary) as ctd_file:
        reader = csv.reader(ctd_file, delimiter="\t")
        row_count = int()
        
        for row in reader:
            row_count += 1
            
            if row_count >= 30:
                term_name = row[0] 
                term_id = row[1][5:]
                synonyms = row[7].split('|')
                name_to_id[term_name] = term_id
                
                for synonym in synonyms:
                    name_to_id[synonym] = term_id
    
    return name_to_id
    

def load_decs_spa():
    """ Loads Spanish DeCS vocabulary"""

    print("Loading ES DeCS...")
    
    graph = obonet.read_obo("./data/kbs/DeCS_2019.obo") # Load the ontology from local file
    graph = graph.to_directed()
    name_to_id = dict()

    for node in  graph.nodes(data=True):
        node_id, node_name = node[0], node[1]["name"]
        name_to_id[node_name] = node_id
            
        if "synonym" in node[1].keys(): # Check for synonyms for node (if they exist)
                
            for synonym in node[1]["synonym"]:
                synonym_name = synonym.split("\"")[1]
                name_to_id[synonym_name] = node_id
   
    return name_to_id


def load_decs_pt(branch):
    
    name_to_id = dict()
    
    return name_to_id