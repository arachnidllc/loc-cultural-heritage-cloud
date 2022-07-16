import json
# An example script how a dataset can be created out of collection's items data.
from datasets import Dataset

with open('./output/output_example.json', 'r') as f:
    data = json.load(f)


ds_dict = {'historic-american-buildings-landscapes-and-engineering-records': data['items']}
dataset_example = Dataset.from_dict(ds_dict)
