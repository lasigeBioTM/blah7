# 1. Document Retrieval

The module retrieves abstracts related with COVID-19 rom [PubMed](https://pubmed.ncbi.nlm.nih.gov/) repository using [Bio.Entrez package](https://biopython.org/docs/1.75/api/Bio.Entrez.html). 

There are two different datasets:
    
- ***abstracts_covid_19***: includes abstracts directly related with COVID-19. Query: "covid-19"
    
- ***abstracts_large***: includes abstracts directly and indirectly related with COVID-19. Query: "2019 Novel Coronavirus Disease OR 2019 Novel Coronavirus Infection OR 2019-nCoV Disease OR 2019-nCoV Infection OR COVID-19 Pandemic OR COVID-19 Pandemics OR COVID-19 Virus Disease OR COVID-19 Virus OR Infection OR COVID19 OR Coronavirus Disease 2019 OR Coronavirus Disease-19 OR SARS Coronavirus 2 Infection OR SARS-CoV-2 Infection"

For each dataset, it is generated the following sets:
- **en+pt**: abstracts in English ("en") and Portuguese ("pt"). To the above queries the following terms were appended at the end: "AND English [LANG] AND Portuguese [LANG]"

- **en+spa**: abstracts in English ("en") and Spanish ("spa"). To the above queries the following terms were appended at the end: "AND English [LANG] AND Spanish [LANG]"

The following command executes the script "retrieve_abstracts.py":

```python retrieve_abstracts.py <language> <version>```

Args:
    - *language*: the selected 2nd language besides English, either "pt" or "spa"
    - *version*: the dataset to build, either 'covid_19' or 'large'

Example:

``
python retrieve_abstracts pt covid_19
``

The dir '../abstracts_covid_19/en+pt' will include the output files. 
