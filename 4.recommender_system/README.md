# BLAH7: Annotating a multilingual COVID-19-related corpus - recommender system

# How to create the recommendation datasets 
* config file in /create_datasets/config/config.ini

*  In create_datasets/src run:

```
python create_blah7_rec_dataset.py
```

* output:

    Two csv files with the columns:
            
            <user_id, item_id, rating>
            <user_name, item_id, rating, user_id>

* The folder data_example contains:
    * 