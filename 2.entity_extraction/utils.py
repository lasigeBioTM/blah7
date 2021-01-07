import csv
import obonet
import os
import sys
import xml.etree.ElementTree as ET

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
                term_id = "https://id.nlm.nih.gov/mesh/"+ row[1][5:]
                synonyms = row[7].split('|')
                name_to_id[term_name] = term_id
                
                for synonym in synonyms:
                    name_to_id[synonym] = term_id
    
    return name_to_id
    

def load_decs_spa():
    """Loads Spanish DeCS .tsv file"""

    print("Loading ES DeCS...")
    
    graph = obonet.read_obo("DeCS_2019.obo") # Load the ontology from local file
    graph = graph.to_directed()
    name_to_id = dict()

    for node in  graph.nodes(data=True):
        node_id, node_name = "https://id.nlm.nih.gov/mesh/" + node[0], node[1]["name"] 
        name_to_id[node_name] = node_id
            
        if "synonym" in node[1].keys(): # Check for synonyms for node (if they exist)
                
            for synonym in node[1]["synonym"]:
                synonym_name = synonym.split("\"")[1]
                name_to_id[synonym_name] = node_id
   
    return name_to_id


def load_decs_xml(language):
    """Loads DeCS vocabulary .xml file in selected language"""
    
    name_to_id = dict()

    if language == "pt":
        filepath = "../data/kbs/bireme_decs_por2020.xml"
    elif language == "spa":
        filepath = "../data/kbs/bireme_decs_spa2020.xml"
    elif language == "en":
        filepath = "../data/kbs/bireme_decs_eng2020.xml"
    
    root = ET.parse(filepath)
    
    for descriptor in root.iter("DescriptorRecord"):
        descriptor_id_found, descriptor_name_found = False, False
        descriptor_text, descriptor_id = str(), str()

        for child in descriptor:
            
            if not descriptor_id_found or not descriptor_name_found:
                
                if child.tag == "DescriptorUI":
                    
                    if "DDCS0" not in child.text: #mesh descriptor; excludes exclusively decs descriptors not present in mesh
                        descriptor_id = "https://id.nlm.nih.gov/mesh/" + child.text
                        descriptor_id_found = True

                elif child.tag == "DescriptorName":
                    
                    descriptor_name_found = True
                    descriptor_name = child.find("String").text[5:].rstrip().split("[")[0]
        
        if descriptor_id_found and descriptor_name_found:
            name_to_id[descriptor_name] = descriptor_id    
    
    return name_to_id