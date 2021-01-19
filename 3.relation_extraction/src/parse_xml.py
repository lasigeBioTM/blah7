import os
import xml.etree.ElementTree as ET
import json

import process_results


def relations_json(corpus_path, results_file, destination_path):
    """

    :param corpus_path:
    :param results_file:
    :param destination_path:
    :return:
    """

    e_dict_name, e_dict_id = process_results.process_entities(corpus_path)

    results = open(results_file, 'r')
    results.readline()
    results_lines = results.readlines()
    results.close()

    for filename in os.listdir(corpus_path):
        data = {}

        tree = ET.parse(corpus_path + '/' + filename)
        root = tree.getroot()

        for sentence in root:

            data['text'] = sentence.get('text')
            data['denotations'] = []
            for e in sentence.findall('entity'):
                data['denotations'].append({'id': e.get('ontology_id'),
                                            "span":{"begin":int(e.get('charOffset').split('-')[0]),'end':int(e.get('charOffset').split('-')[1])},
                                            "obj":e.get('text')})

            data['relations'] = []
            id = 0
            for results_line in results_lines:
                if sentence.get('id').split('.')[0] == results_line.split('\t')[0].split('.')[0]:
                    data['relations'].append({'id':'R' + str(id), 'subj':e_dict_id[results_line.split('\t')[0]], 'pred':results_line.split('\t')[2][:-1], 'obj':e_dict_id[results_line.split('\t')[1]]})
                    id += 1

        with open(destination_path + filename.split('.')[0] + '_relations.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)

    return

def join_results(corpus_paths, destination_path):
    """

    :param corpus_paths:
    :param destination_path:
    :return:
    """

    for filename in os.listdir(corpus_paths[0]):
        data = {}

        with open(corpus_paths[0] + filename) as json_file:
            content = json.load(json_file)
            data['text'] = content['text']

        data['denotations'] = []
        data['relations'] = []
        for corpus_path in corpus_paths:
            with open(corpus_path + filename) as json_file:
                content = json.load(json_file)
                data['denotations'].extend(content['denotations'])
                data['relations'].extend(content['relations'])

        data['denotations'] = sorted(data['denotations'], key=lambda k: k['span']['begin'])
        data_relations = []
        id_relation = 0
        for relation in data['relations']:
            new_relation = {'id': 'R' + str(id_relation), 'subj': relation['subj'], 'pred': relation['pred'], 'obj': relation['obj']}
            id_relation += 1
            data_relations.append(new_relation)
        data['relations'] = data_relations
        with open(destination_path + filename.split('.')[0] + '.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)

    return

#### RUN ####

def main():
    """Generates a relations file in json
    """

    #relations_json('corpora/go_phenotype_xml_blah/', 'results/model_ontologies_go_phenotype_results_blah.txt','results/relations_json_go_phenotype/')
    #relations_json('corpora/drug_disease_xml_blah/', 'results/model_ontologies_drug_disease_results_blah.txt', 'results/relations_json_drug_disease/')
    join_results(['results/relations_json_go_phenotype/','results/relations_json_drug_disease/'], 'results/relations_json_all/')

    return


# python3 src/process_results.py
if __name__ == "__main__":
    main()