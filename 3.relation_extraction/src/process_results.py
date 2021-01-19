import os
import xml.etree.ElementTree as ET


def process_entities(corpus_path):
    """

    :param corpus_path:
    :return:
    """

    e_dict_name = {}
    e_dict_id = {}
    for filename in os.listdir(corpus_path):

        tree = ET.parse(corpus_path + '/' + filename)
        root = tree.getroot()

        for sentence in root:
            for e in sentence.findall('entity'):
                e_id = e.get('id')
                e_name = e.get('text')
                e_ontology_id = e.get('ontology_id')
                e_dict_name[e_id] = e_name
                e_dict_id[e_id] = e_ontology_id

    return e_dict_name, e_dict_id

def process_results_individual(corpus_path, results_file, destination_file_names, destination_file_identifiers):
    """

    :param corpus_path:
    :param results_file:
    :param destination_file_names:
    :param destination_file_identifiers:
    :return:
    """

    e_dict_name, e_dict_id = process_entities(corpus_path)

    results_names = open(destination_file_names, 'w')
    results_identifiers = open(destination_file_identifiers, 'w')

    results = open(results_file, 'r')
    header = results.readline()  # skip header
    results_names.write(header)
    results_identifiers.write(header)
    results_lines = results.readlines()
    results.close()

    for result in results_lines:
        entity_1_result_id = result.split('\t')[0]
        entity_2_result_id = result.split('\t')[1]

        results_names.write(e_dict_name[entity_1_result_id] + '\t' + e_dict_name[entity_2_result_id] + '\t' + result.split('\t')[2])
        results_identifiers.write(e_dict_id[entity_1_result_id] + '\t' + e_dict_id[entity_2_result_id] + '\t' + result.split('\t')[2])

    results_names.close()
    results_identifiers.close()

    return

def join_results(results_path, destination_file):
    """

    :param results_path:
    :param destination_file:
    :return:
    """

    joint_names = open(results_path + '/' + destination_file + '_names.tsv', 'w')
    joint_names.write('Entity_1\tEntity_2\tPredicted_class' + '\n')
    joint_identifiers = open(results_path + '/' + destination_file + '_identifiers.tsv', 'w')
    joint_identifiers.write('Entity_1\tEntity_2\tPredicted_class' + '\n')

    for filename in os.listdir(results_path):
        if filename.endswith('names.tsv'):
            results_file = open(results_path + '/' + filename, 'r')
            results_file.readline()
            results_file_lines = results_file.readlines()
            for line in results_file_lines:
                joint_names.write(line)
            results_file.close()

        elif filename.endswith('identifiers.tsv'):
            results_file = open(results_path + '/' + filename, 'r')
            results_file.readline()
            results_file_lines = results_file.readlines()
            for line in results_file_lines:
                joint_identifiers.write(line)
            results_file.close()

    joint_names.close()
    joint_identifiers.close()

    return


#### RUN ####

def main():
    """Generates a results file with the entities names
    """

    #process_results_individual('corpora/go_phenotype_xml_100/', 'results/model_ontologies_go_phenotype_results_100.txt',
    #                           'results/go_phenotype_100_relations_names.tsv', 'results/go_phenotype_100_relations_identifiers.tsv')
    #process_results_individual('corpora/drug_disease_xml_100/', 'results/model_ontologies_drug_disease_results_100.txt',
    #                           'results/drug_disease_100_relations_names.tsv',
    #                           'results/drug_disease_100_relations_identifiers.tsv')
    process_results_individual('corpora/drug_disease_xml/', 'results/model_ontologies_drug_disease_results.txt',
                               'results/drug_disease_relations_names.tsv',
                               'results/drug_disease_relations_identifiers.tsv')
    process_results_individual('corpora/go_phenotype_xml/', 'results/model_ontologies_go_phenotype_results.txt',
                               'results/go_phenotype_relations_names.tsv',
                               'results/go_phenotype_relations_identifiers.tsv')
    join_results('results', 'joint_results')

    return


# python3 src/process_results.py
if __name__ == "__main__":
    main()