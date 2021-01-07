import json
import os
import merpy
import multiprocessing
import sys
import tqdm
import re
from collections import Counter
from itertools import chain
from utils import load_ctd_vocabularies, load_decs_xml
sys.path.append("./")

global_entities = Counter()


def process_doc(doc_file, lexicons, output_dir):
    """
    Open one json file with one doc, run merpy with lexicons and write results to file

    """
    
    with open(doc_file, "r") as f_in:
        doc = json.load(f_in)
    
    new_doc = {
        "id": doc["paper_id"],
        "entities": {},
        "sections": {"title": [], "abstract": []}
    }

    # iterate through title and abtract
    title = doc["metadata"]["title"]
    
    new_doc["sections"]["title"] = process_multiple_docs_lexicons_sp([title], active_lexicons)
    new_doc["sections"]["title"] = new_doc["sections"]["title"][0]

    abstract = [p["text"] for p in doc["abstract"]]
    new_doc["sections"]["abstract"] = process_multiple_docs_lexicons_sp(abstract, active_lexicons)

    # count all URI
    all_uris = [e[3] for e in new_doc["sections"]["title"] if len(e) > 3]
    all_uris += [e[3] for e in chain.from_iterable(new_doc["sections"]["abstract"]) if len(e) > 3]

    # get counter of URIs and sort by value
    doc_counter = Counter(all_uris)
    new_doc["entities"] = {
        k: v
        for k, v in sorted(doc_counter.items(), key=lambda item: item[1], reverse=True)
    }

    print("top doc", doc_counter.most_common(10))
    
    with open(
        output_dir + doc_file.split("/")[-1].split(".")[0] + "_entities.json", "w"
    ) as f_out:
        json.dump(new_doc, f_out, indent=4, ensure_ascii=False)
    
    return doc_counter


def repl(m):
    # replace all matches with "a"
    return "a" * len(m.group())


def process_multiple_docs_lexicons_sp(docs, lexicons):
    """
    Iterate through list of doc directories
    """
    # create one empty list for each doc
    doc_dict = {i: d for i, d in enumerate(docs)}
    output_entities = [[]] * len(docs)
    doc_results = []
    
    for idoc, doc in enumerate(docs):
    
        if sum(map(str.isalnum, doc)) < 5:  # must have at least 5 alnum
            print("no words", doc)
            continue
    
        doc = re.sub(r"[^A-Za-z0-9 ]{2,}", repl, doc)
    
        for l in lexicons:
            doc_results += merpy.get_entities(doc, l)
    
        for e in doc_results:
            # doc_entities = merpy.get_entities_mp(doc_dict, lex, n_cores=10)
            # print(lex, entities)
            # for e in l_entities:
            if len(e) > 2:
                entity = [int(e[0]), int(e[1]), e[2]]
                if len(e) > 3:  # URI
                    entity.append(e[3])
                if entity not in output_entities[idoc]:
                    output_entities[idoc].append(entity)
    
    for i in range(len(output_entities)):
        output_entities[i] = sorted(output_entities[i])
    
    return output_entities


def process_lexicons_4_mer():
    
    print("download latest obo files")
    merpy.download_lexicon("http://purl.obolibrary.org/obo/doid.owl", "do", ltype="owl")
    merpy.download_lexicon("http://purl.obolibrary.org/obo/go.owl", "go", ltype="owl")
    merpy.download_lexicon("http://purl.obolibrary.org/obo/hp.owl", "hpo", ltype="owl")
    merpy.download_lexicon("ftp://ftp.ebi.ac.uk/pub/databases/chebi/ontology/chebi.owl", "chebi", ltype="owl")
    merpy.download_lexicon("http://purl.obolibrary.org/obo/ncbitaxon.owl", "taxon", ltype="owl")
    merpy.download_lexicon("https://raw.githubusercontent.com/CIDO-ontology/cido/master/src/ontology/cido.owl", 
            "cido",
            "owl",
    )

    print("process lexicons")
    merpy.process_lexicon("do", ltype="owl")
    merpy.process_lexicon("go", ltype="owl")
    merpy.process_lexicon("hpo", ltype="owl")
    merpy.process_lexicon("chebi", ltype="owl")
    merpy.process_lexicon("taxon", ltype="owl")
    merpy.process_lexicon("cido", "owl")
    
    #Delete obsolete entities
    merpy.delete_obsolete("do")
    merpy.delete_obsolete("go")
    merpy.delete_obsolete("hpo")
    merpy.delete_obsolete("chebi")
    merpy.delete_obsolete("taxon")
    merpy.delete_obsolete("cido")
       
    merpy.delete_entity("protein", "chebi")
    merpy.delete_entity("protein", "cido")
    merpy.delete_entity("protein", "hpo")
    merpy.delete_entity("polypeptide chain", "chebi")
    merpy.delete_entity("data", "taxon")
    merpy.delete_entity("one", "chebi")
    merpy.delete_entity_by_uri("http://purl.obolibrary.org/obo/PATO_0000070", "hpo")
    
    #Create and process english vocabularies
    #lexicon_name = "medic"
    #medic_name_to_id = load_ctd_vocabularies("CTD_diseases.tsv")
    #merpy.create_lexicon(medic_name_to_id.keys(), lexicon_name)
    #merpy.create_mappings(medic_name_to_id, lexicon_name)
    #merpy.process_lexicon(lexicon_name)

    #lexicon_name = "ctdChemicals"
    #chemicals_name_to_id = load_ctd_vocabularies("CTD_chemicals.tsv")
    #merpy.create_lexicon(chemicalsbireme_decs_spa2020.xm_name_to_id.keys(), lexicon_name)
    #merpy.create_mappings(chemicals_name_to_id, lexicon_name)
    #merpy.process_lexicon(lexicon_name)

    #lexicon_name = "ctdAnatomy"
    #anatomy_name_to_id = load_ctd_vocabularies("CTD_anatomy.tsv")
    #merpy.create_lexicon(anatomy_name_to_id.keys(), lexicon_name)
    #merpy.create_mappings(anatomy_name_to_id, lexicon_name)
    #merpy.process_lexicon(lexicon_name)
    
    ##Create and process english decs 
    lexicon_name = "decsEN"
    name_to_id_spa = load_decs_xml("en")
    merpy.create_lexicon(name_to_id_spa.keys(), lexicon_name)
    merpy.create_mappings(name_to_id_spa, lexicon_name)
    merpy.process_lexicon(lexicon_name)

    ##Create and process spanish decs
    lexicon_name = "decsSPA"
    name_to_id_spa = load_decs_xml("spa")
    merpy.create_lexicon(name_to_id_spa.keys(), lexicon_name)
    merpy.create_mappings(name_to_id_spa, lexicon_name)
    merpy.process_lexicon(lexicon_name)
   
    #Create and process portuguese decs
    lexicon_name = "decsPT"
    name_to_id_spa = load_decs_xml("pt")
    merpy.create_lexicon(name_to_id_spa.keys(), lexicon_name)
    merpy.create_mappings(name_to_id_spa, lexicon_name)
    merpy.process_lexicon(lexicon_name)

if __name__ == "__main__":

    mode = str(sys.argv[1])
    input_dir = str(sys.argv[2])
    
    if mode == "annotate":
        language = input_dir.split("/")[3]#str(sys.argv[2]) # "en", "pt" or "spa"
    
    if mode == "setup": # update MER
       process_lexicons_4_mer()

    elif mode == "annotate":
        active_lexicons = list()

        if language == "en":
            active_lexicons = ["do", "go", "hpo", "chebi", "taxon", "cido", "decsEN"]#"medic", "ctdChemicals", "ctdAnatomy"]
            
        elif language == "pt":
            active_lexicons = ["decsPT"]

        elif language == "spa":
            active_lexicons = ["decsSPA"]

        output_dir = input_dir.rstrip("/") + "_entities/"

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        print("processing docs")

        with multiprocessing.Pool(processes=10) as pool:
            doc_entities = pool.starmap(
                process_doc,
                [
                    (input_dir + "/" + d, active_lexicons, output_dir)
                    for d in os.listdir(input_dir)
                ],
            )
            for entities in doc_entities:
                global_entities.update(entities)

            entities_by_uri = {}

            print()
            print("global top", global_entities.most_common(10))
            print("total", sum(global_entities.values()))
