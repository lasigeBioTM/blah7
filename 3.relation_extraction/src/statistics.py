import os


def statistics(corpus_path):
    """

    :param corpus_path:
    """

    save_pairs = []
    for (dir_path, dir_names, file_names) in os.walk(corpus_path):
        for filename in file_names:

            annotation_file = open(corpus_path + filename.split('.')[0] + '.txt', 'r')
            annotation_file_lines = annotation_file.readlines()

            for line in annotation_file_lines:
                if 'HP-' in line or 'GO-' in line or 'DOID-' in line or 'CHEBI-' in line:
                    line_elements = line.split('\t')
                    save_pairs.append(line_elements[1])

    print('HP-HP', save_pairs.count('HP-HP'), 'GO-GO', save_pairs.count('GO-GO'), 'DOID-DOID', save_pairs.count('DOID-DOID'),
          'CHEBI-CHEBI', save_pairs.count('CHEBI-CHEBI'), 'CHEBI-HP', save_pairs.count('CHEBI-HP') + save_pairs.count('HP-CHEBI'),
          'GO-HP', save_pairs.count('GO-HP') + save_pairs.count('HP-GO'), 'CHEBI-DOID', save_pairs.count('CHEBI-DOID') + save_pairs.count('DOID-CHEBI'),
          'GO-CHEBI', save_pairs.count('GO-CHEBI') + save_pairs.count('CHEBI-GO'), 'GO-DOID', save_pairs.count('GO-DOID') + save_pairs.count('DOID-GO'),
          'HP-DOID', save_pairs.count('HP-DOID') + save_pairs.count('DOID-HP'))

statistics('corpora/original_text_txt_10/')
