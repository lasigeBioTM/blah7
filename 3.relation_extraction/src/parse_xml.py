import os
import xml.etree.ElementTree as ET
import json


def relations_json(corpus_path, results_file, destination_path):
    """

    :param corpus_path:
    :param results_file:
    :param destination_path:
    :return:
    """

    results = open(results_file, 'r')
    results.readline()
    results_lines = results.readlines()
    results.close()

    dict_entities = {}
    for filename in os.listdir(corpus_path):
        data = {}

        tree = ET.parse(corpus_path + '/' + filename)
        root = tree.getroot()

        for sentence in root:

            if sentence.get('id').endswith('c1'):
                data['text'] = sentence.get('text')
                data['denotations'] = []
                identifier = 0
                for e in sentence.findall('entity'):
                    data['denotations'].append({'id': 'T' + str(identifier),
                                                "span": {"begin":int(e.get('charOffset').split('-')[0]),'end':int(e.get('charOffset').split('-')[1])},
                                                "obj": e.get('ontology_id')})
                    entity_identifier = e.get('id')

                    ### individual:
                    #dict_entities[entity_identifier] = 'T' + str(identifier)
                    ### multiple:
                    dict_entities[entity_identifier] = ['T' + str(identifier),{"begin":int(e.get('charOffset').split('-')[0]),'end':int(e.get('charOffset').split('-')[1])},e.get('ontology_id')]
                    ###
                    identifier += 1

                data['relations'] = []
                id = 0
                for results_line in results_lines:
                    if sentence.get('id') == results_line.split('\t')[0].split('.')[0] + '.' + results_line.split('\t')[0].split('.')[1]:
                        ### individual:
                        #data['relations'].append({'id':'R' + str(id), 'subj':dict_entities[results_line.split('\t')[0]], 'pred':results_line.split('\t')[2][:-1], 'obj':dict_entities[results_line.split('\t')[1]]})
                        ### multiple:
                        data['relations'].append(
                            {'id': 'R' + str(id), 'subj': results_line.split('\t')[0],
                             'pred': results_line.split('\t')[2][:-1],
                             'obj': results_line.split('\t')[1]})
                        ###
                        id += 1

        with open(destination_path + filename.split('.')[0] + '_relations.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)

    return dict_entities

def join_results(corpus_paths, destination_path, dict_entities):
    """

    :param corpus_paths:
    :param destination_path:
    :param dict_entities:
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
        data_denotations = []

        id_denotation = 0
        dict_old_new = {}
        for denotation in data['denotations']:
            new_denotation = {'id': 'T' + str(id_denotation),
                              "span": denotation['span'],
                              "obj": denotation['obj']}

            for items in dict_entities.items():
                if items[1] == [denotation['id'], denotation['span'], denotation['obj']]:
                    dict_old_new[items[0]] = ['T' + str(id_denotation), denotation['span'], denotation['obj']]

            id_denotation += 1
            data_denotations.append(new_denotation)


        data['denotations'] = data_denotations
        data_relations = []
        id_relation = 0

        for relation in data['relations']:

            new_relation = {'id': 'R' + str(id_relation), 'subj': dict_old_new[relation['subj']][0], 'pred': relation['pred'], 'obj': dict_old_new[relation['obj']][0]}

            id_relation += 1
            data_relations.append(new_relation)
        data['relations'] = data_relations

        data['sourcedb'] = 'PubMed@dpavot'
        data['sourceid'] = filename.split('.')[0]
        with open(destination_path + filename.split('.')[0] + '.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)

    return

#### RUN ####

def main():
    """Generates a relations file in json
    """

    dict_entities_gp = relations_json('corpora/go_phenotype_xml_blah/', 'results/model_ontologies_go_phenotype_results_blah.txt','results/relations_json_go_phenotype/')
    dict_entities_ddo = relations_json('corpora/drug_disease_xml_blah/', 'results/model_ontologies_drug_disease_results_blah.txt', 'results/relations_json_drug_disease/')
    dict_entities = {**dict_entities_gp, **dict_entities_ddo}
    join_results(['results/relations_json_go_phenotype/','results/relations_json_drug_disease/'], 'results/relations_json_all/', dict_entities)

    return


# python3 src/process_results.py
if __name__ == "__main__":
    main()