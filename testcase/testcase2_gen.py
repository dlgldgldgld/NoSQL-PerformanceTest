import json
import csv

from faker import Faker
from faker.providers import lorem
from collections import namedtuple

index_space = {
  "index": {
    "_index": "posts",
    "_type": "test",
    "_id": None
  }
}

file_schema = {
    "title" : None,
    "content" : None
}

csv_schema = namedtuple(
    'csv_schema', ['title', 'content'])

Faker.seed(5)
fake = Faker()
id = 0

json_4_es = open('elastic_import.json', 'w', newline="")
json_4_fts = open('fts_import.csv', 'w', newline='')
csv_writer = csv.writer(json_4_fts)

for _ in range(100000):
    id += 1
    index_space["index"]["_id"] = str(id)
    file_schema["title"] = fake.word()
    file_schema["content"] = fake.paragraph(nb_sentences=5)

    json.dump(index_space, json_4_es)
    json_4_es.write('\n')
    json.dump(file_schema, json_4_es)
    json_4_es.write('\n')
    csv_writer.writerow([file_schema["title"], file_schema["content"]])

json_4_es.close()
json_4_fts.close()