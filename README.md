# BLAH7: Annotating a multilingual COVID-19-related corpus

## Group Information

- **Authors:** Márcia Barros, Pedro Ruas, Diana Sousa, and Francisco M. Couto
- **E-mail addresses:** (*mcbarros*, *psruas*, *dfsousa*, *fjcouto*)@fc.ul.pt
- **Instituition:** LASIGE, Faculdade de Ciências, Universidade de Lisboa, Portugal

## How the Annotations are Developed
The first step is the generation of a silver standard by applying our [COVID text mining pipeline](https://github.com/lasigeBioTM/knowledge-extraction-from-CORD-19), which includes three modules: **Entity extraction**, **Relation extraction**, and **Recommender system**. The Entity Extraction module recognizes disease, chemical, and anatomical entities and links them to the respective MeSH identifier. The Relation Extraction module recognizes candidate relations between those entities. We are particularly interested in negative relations where there is already evidence of no association to prevent researchers from pursuing already refuted research hypotheses, and focus their research.  The Recommender System module creates a dataset of user, item, rating, where the users are authors from the research documents related to COVID-19, the items are the entities extracted in the entity extraction phase, and the ratings are the number of articles in which the author mentioned the entity.
The second step consists of the manual correction of the annotations in a selected subset of the silver standard, and in the addition of missing annotations.

### Methodology 

The **first part** consists of the document retrieval by two different approaches:
- Download of .tsv file with [LitCovid citations](https://www.ncbi.nlm.nih.gov/research/coronavirus/#data-download)
Consider the PMIDs in the file, retrieve the respective abstracts from PubMed using the available API, and filter those with English and Spanish abstracts simultaneously (or English and Portuguese) 

Or instead:

 - Retrieve PubMed articles with the available API using the search profile: new coronavirus* OR novel coronavirus* OR ncov OR sars-cov OR covid* OR cov-2 OR cov-19 and then filter those with English and Spanish abstracts simultaneously (or English and Portuguese)


The **second part** consists of the application of the COVID text mining pipeline.
The Entity Extraction module performs NER by applying the MER tool, which can recognize Disease, Chemical, Anatomy entities and link them to the respective vocabulary identifiers. On English texts, the recognized entities will be linked to MeSh identifiers using the CTD Disease (MEDIC), CTD Chemical, and CTD Anatomy vocabularies or, in alternative, the Coronavirus Infectious Disease Ontology (CIDO). On Spanish/Portuguese texts the recognized entities will be linked to MeSH identifiers through the DeCS vocabulary.

The Relation Extraction module performs RE by applying the BiOnt system, which was built to allow the extraction of relations between multiple biomedical entities supported by ontologies. Using the MeSh identifiers or the CIDO ontology linked to the recognized Disease, Chemical, Anatomy entities the BiOnt system can identify relations between those entities, provided we can use the pre-trained models trained on available training data. Additionally, the BiOnt system must be adapted to allow the identification of negative relations. 

The recommender system dataset is created through LIBRETTI methodology, which was developed with the goal of creating scientific recommendation dataset using research literature to extract implicit feedback. This dataset allows the recommendation of COVID-19 related entities of interest for a researcher, which could be lost for the researchers in the large number of entities enclosed in the literature.  

### Evaluation

Subset of annotations in the corpus for crowd evaluation

### Pipeline with Example

#  <img src="https://github.com/lasigeBioTM/blah7/blob/main/pipeline.png">

## Global Motivation

The global motivation is the creation of parallel multilingual datasets for text mining systems in COVID-related literature. Tracking the most recent advances in the COVID-related research is essential given the novelty of the disease and its impact on society, but the pace of publication requires automatic approaches in order to access and organize the knowledge that keeps being produced everyday. It is necessary to develop text mining pipelines to assist in that task, which is only possible with evaluation datasets. However, there is a lack of COVID-related datasets, even more if considering other languages besides English. The expected contribution of the project will be the annotation of a multilingual parallel dataset, providing this resource to the community in order to improve the text mining research on COVID-related literature. 

## Goals for BLAH7

- Retrieval of XX COVID-related articles
- Automatically annotation of the articles
- Manual correction of the automatic annotations in a subset of XX articles
- Expansion of the annotations set in the subset

## Relevant Publications


-  Barros, M. A., Lamurias, A., Sousa, D., Ruas, P., & Couto, F. M. (2020). [COVID-19: A Semantic-Based Pipeline for Recommending Biomedical Entities](https://www.aclweb.org/anthology/2020.nlpcovid19-2.20/). In Proceedings of the 1st Workshop on NLP for COVID-19 (Part 2) at EMNLP 2020.
- Sousa, D., Lamurias, A., & Couto, F. M. (*in press*). A Hybrid Approach toward Biomedical Relation Extraction Training Corpora: Combining Distant Supervision with Crowdsourcing. Database.
- Sousa, D., Lamurias, A., & Couto, F. M. (2020). [Improving accessibility and distinction between negative results in biomedical relation extraction
](https://genominfo.org/journal/view.php?number=606&viewtype=pubreader). Genomics & Informatics, 18(2). 
- Sousa, D., Lamurias, A., & Couto, F. M. (2019). [A Silver Standard Corpus of Human Phenotype-Gene Relations](https://www.aclweb.org/anthology/N19-1152/). In Proceedings of the 2019 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long and Short
Papers), pages 1487–1492.



