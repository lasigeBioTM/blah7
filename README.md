# BLAH7: Annotating a multilingual COVID-19-related corpus

## Group Information

- **Authors:** Márcia Barros, Pedro Ruas, Diana Sousa, and Francisco M. Couto
- **E-mail addresses:** (*mcbarros*, *psruas*, *dfsousa*, *fjcouto*)@fc.ul.pt
- **Institution:** LASIGE, Faculdade de Ciências, Universidade de Lisboa, Portugal

## BLAH7 Daily Tasks & Initial Results

### Day 1 (18/01/2021)

Initial meeting to present projects. 

### Day 2 (19/01/2021)

Sample upload of 2.NER/NEL datasets (in [EN](http://pubannotation.org/projects/ENG_NER_NEL) and [PT](http://pubannotation.org/projects/PT_NER_NEL)) and [3.RE dataset](http://pubannotation.org/projects/ENG_RE) (in EN) to PubAnnotation in collection **LASIGE: Annotating a multilingual COVID-19-related corpus for BLAH7** [here](http://pubannotation.org/collections/LASIGE:%20Annotating%20a%20multilingual%20COVID-19-related%20corpus%20for%20BLAH7). 

The 4.recommender system datasets (in EN and PT) are available here on GitHub. 

<p align="center">
  <img src="https://github.com/lasigeBioTM/blah7/blob/main/progress.png">
</p>

### Day 3 (20/01/2021)

Discussion of crowd validation pipeline for the available datasets.

## Global Motivation

The global motivation is the creation of parallel multilingual datasets for text mining systems in COVID-19-related literature. Tracking the most recent advances in the COVID-19-related research is essential given the novelty of the disease and its impact on society. Still, the pace of publication requires automatic approaches to access and organize the knowledge that keeps being produced every day. It is necessary to develop text mining pipelines to assist in that task, which is only possible with evaluation datasets. However, there is a lack of COVID-19-related datasets, even more, if considering other languages besides English. The expected contribution of the project will be the annotation of a multilingual parallel dataset (EN-ES and EN-PT), providing this resource to the community to improve the text mining research on COVID-19-related literature.

Find the video presentation of the project [here](https://drive.google.com/file/d/1QAfdQBBGZylwOQ5K0l5woqQNbWmSoLmq/view?usp=sharing).
## How the Annotations are Developed
We start by generating a silver standard by applying our [COVID text mining pipeline](https://github.com/lasigeBioTM/knowledge-extraction-from-CORD-19), which includes three modules: **entity extraction**, **relation extraction**, and **recommender system**. The entity extraction module recognizes disease, chemical, and anatomical entities and links them to the respective MeSH identifier. The relation extraction module recognizes candidate relations between those entities. We are particularly interested in negative relations where there is already evidence of no association to prevent researchers from pursuing already refuted research hypotheses, and focus their research. The recommender system module creates a dataset of user, item, rating, where the users are authors from the research documents related to COVID-19, the items are the entities extracted in the entity extraction phase, and the ratings are the number of articles in which the author mentioned the entity.
Lastly, we manually correct the annotations in a selected subset of the silver standard and add missing annotations.

### Methodology 

The **first part** consists of the document retrieval by two different approaches:
- Download of .tsv file with [LitCovid citations](https://www.ncbi.nlm.nih.gov/research/coronavirus/#data-download). Consider the PMIDs in the file, retrieve the respective abstracts from PubMed using the available API, and filter those with English and Spanish abstracts simultaneously (or English and Portuguese).

Or instead:

- Retrieve PubMed articles with the available API using the search profile: *new coronavirus\* OR novel coronavirus\* OR ncov OR sars-cov OR covid\* OR cov-2 OR cov-19* and then filter those with English and Spanish abstracts simultaneously (or English and Portuguese)

The **second part** consists of the application of the COVID-19 text mining pipeline. The entity extraction module performs NER by applying the MER tool, which can recognize Disease, Chemical, Anatomy entities and link them to the respective vocabulary identifiers. On English texts, the recognized entities will be linked to MeSh identifiers using the *CTD Disease (MEDIC)*, *CTD Chemical*, and *CTD Anatomy* vocabularies or, in alternative, the *Coronavirus Infectious Disease Ontology (CIDO)*. On Spanish/Portuguese texts the recognized entities will be linked to MeSH identifiers through the DeCS vocabulary.

The **third part** regards the relation extraction module which performs RE by applying the BiOnt system, which was built to allow the extraction of relations between multiple biomedical entities supported by ontologies. Using the MeSh identifiers or the CIDO ontology linked to the recognized Disease, Chemical, Anatomy entities the BiOnt system can identify relations between those entities, provided we can use the pre-trained models trained on available training data. Additionally, the BiOnt system must be adapted to allow the identification of negative relations. 

Finally, in the **fourth part**, the recommender system dataset, is created through LIBRETTI methodology, which was developed with the goal of creating scientific recommendation dataset using research literature to extract implicit feedback. 
This dataset allows the recommendation of COVID-19 related entities of interest for a researcher, which could be lost for the researchers in the large number of entities enclosed in the literature.  



### Evaluation

Subset of annotations in the corpus for crowd evaluation.

The recommendation dataset is evaluated in two phases, first automatically, testing the dataset before and after the 
curation of the previous phases (NER and RE), and second, manually, with experts testing if the recommendation are 
suitable for the users, according to their previous preferences.

### Pipeline with Example (PMID:33220478)

#  <img src="https://github.com/lasigeBioTM/blah7/blob/main/pipeline.png">

## Goals for BLAH7

- Retrieval of a sample of COVID-related articles;
- Automatically annotation of the articles;
- Manual correction of the automatic annotations in a subset the articles;
- Expansion of the annotations set in the subset;
- Automatic evaluation of the recommendation dataset;
- Manual evaluation of the recommendation dataset.

## Relevant Publications

-  Barros, M. A., Lamurias, A., Sousa, D., Ruas, P., & Couto, F. M. (2020). [COVID-19: A Semantic-Based Pipeline for Recommending Biomedical Entities](https://www.aclweb.org/anthology/2020.nlpcovid19-2.20/). In Proceedings of the 1st Workshop on NLP for COVID-19 (Part 2) at EMNLP 2020.
- Barros, M., Moitinho., A., & Couto, F. M.  (2019). [Using research literature to generate datasets of implicit feedback for recommending scientific items.](https://ieeexplore.ieee.org/abstract/document/8924687) IEEE Access 7: 176668-176680.
- Sousa, D., Lamurias, A., & Couto, F. M. (2020). [A Hybrid Approach toward Biomedical Relation Extraction Training Corpora: Combining Distant Supervision with Crowdsourcing](https://academic.oup.com/database/article/doi/10.1093/database/baaa104/6013761?login=true). Database 2020.
- Sousa, D., Lamurias, A., & Couto, F. M. (2020). [Improving accessibility and distinction between negative results in biomedical relation extraction](https://genominfo.org/journal/view.php?number=606&viewtype=pubreader). Genomics & Informatics, 18(2). 
- Sousa, D., Lamurias, A., & Couto, F. M. (2019). [A Silver Standard Corpus of Human Phenotype-Gene Relations](https://www.aclweb.org/anthology/N19-1152/). In Proceedings of the 2019 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long and Short Papers), pages 1487–1492.
- Couto, F. & Lamurias, A. (2018). [MER: a Shell Script and Annotation Server for Minimal Named Entity Recognition and Linking](https://doi.org/10.1186/s13321-018-0312-9). Journal of Cheminformatics, 10:58, 2018. 



