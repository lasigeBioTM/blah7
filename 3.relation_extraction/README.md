# 3. Relation Extraction

This module uses the entities extracted in module 2.entity_extraction to perform relation extraction. Specifically using the CHEBI, HPO, DO, and GO ontologies.

We used [BiOnt](https://github.com/lasigeBioTM/BiOnt) to perform the main steps towards a relation extraction corpus.

#### Auxiliary scripts:

- ***blacklist.py***: list of badly identified NER entities.
- ***parse_json.py***: convert *json* format to *xml* and *txt*.
- ***parse_xml.py***: convert *tsv* results back to *json*.
- ***process_results.py***: process results to 4.recommender systems.
- ***statistics.py***: counts of the number of annotations.

For more information, contact *dfsousa@lasige.di.fc.ul.pt* or raise an issue.
