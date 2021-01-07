# 2. Entity Extraction (Named Entity Recognition + Linking)

This module extracts entities present in the retrieved documents and it is based on python implementation of [MER](https://pypi.org/project/merpy/).

Requirements:
-[merpy](https://pypi.org/project/merpy/)>=1.7.1

In English abstracts, extracted entities are linked to concepts of the following ontologies (latest versions available as of January 2020, apart from):   

- [Disease Ontology](https://disease-ontology.org/) ("do")
- [Gene Ontology](http://geneontology.org/) ("go")
- [Human Phenotype Ontology](https://hpo.jax.org/app/) ("hpo")
- [ChEBI ontology](https://www.ebi.ac.uk/chebi/) ("chebi")
- [NCBI taxonomy](https://www.ncbi.nlm.nih.gov/taxonomy) ("taxon")
- [DeCS](https://decs.bvsalud.org/en/) (September 2020 version - "decsEN")

In Portuguese and Spanish abstracts, extracted entities are linked to concepts of the respective version of [DeCS](https://decs.bvsalud.org/en/) (September 2020 versions), respectively, "decsPT" and "decsSPA".

The following command executes the script "mer_entities.py":

```
python mer_entities.py <mode> <input_dir>
```

Args:
- *mode*: if "setup" processes lexicons for MER. Set to "annotate" if lexicons already processed in a previous run.
- *input_dir*: the directory containing the documents to be annotated.     

Example for lexicon processing:

```
python mer_entities.py setup ''
```

Example for document annotation:
```
python mer_entities.py annotate ../abstracts_covid_19/en+pt/pt
```

The dir '../abstracts_covid_19/en+pt/pt_entities' will include the output files. 
