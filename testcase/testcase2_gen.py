import json
from faker import Faker
from faker.providers import lorem

index_space = {
  "index": {
    "_index": "classes",
    "_type": "class",
    "_id": None
  }
}

file_schema = {
    "title" : None,
    "content" : None
}

Faker.seed(5)
fake = Faker()
id = 0

json_4_es = open('elastic_import.json', 'w', newline="")

for _ in range(10):
    id += 1
    index_space["index"]["_id"] = str(id)
    file_schema["title"] = fake.word()
    file_schema["content"] = fake.paragraph(nb_sentences=5)

    json.dump(index_space, json_4_es)
    json_4_es.write('\n')
    json.dump(file_schema, json_4_es)
    json_4_es.write('\n')

json_4_es.close()