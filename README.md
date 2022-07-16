### loc parser project

A scrapy crawler to parse and save data from the Library of Congress API.

### How to use:

1. Clone the repository
2. Setup virtual environment (`pipenv` recomended, see [here](https://pipenv.pypa.io/en/latest/))
3. Run `pipenv install`, then activate with `pipenv shell`
4. Use the `scrapy crawl` command to run spider for a specific collection. For example:

```bash
scrapy crawl loc_collections -a "url=https://www.loc.gov/collections/historic-american-buildings-landscapes-and-engineering-records/?c=150&at!=content,pages&fo=json" -a "items_limit=500"
```
5. Use the `scrapy crawl` command to run spider to save specific item images. For example:
```bash
scrapy crawl loc_item_images -a "fn=./output/output_example.json"
```
images will be saved in following path:
```
./output/{item_id}/{image_id}.jpg
```

### Future improvements
1. Create collections parameters mapping so users only have to specify the collection name, e.g.:
```bash
scrapy crawl loc_collections -a "cn=copland" -a "items_limit=500"
scrapy crawl loc_collections -a "cn=fwp" -a "items_limit=500"
...
etc.
```
2. Create scalable, deployable and more robust infrastructure to parse, process and store data.
3. Create pipeline for creating `datasets` out of parsed collections data. See https://github.com/huggingface/datasets/blob/main/templates/README_guide.md
4. Use cloud storage to saving items, images and documents.
