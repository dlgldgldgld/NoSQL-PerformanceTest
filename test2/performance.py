from elasticsearch import Elasticsearch
import time

import sqlite3

def get_title_es(keyword = ""):
    start = time.perf_counter()
    
    es = Elasticsearch(hosts='http://localhost:9200')
    resp = es.search(index="posts", size=10000, query={"match" : { "content" : keyword}})
    result = []
    for hit in resp['hits']['hits']:
        result.append(hit['_source']['title'])

    end = time.perf_counter()
    return result, round(end-start,3)

def get_title_sqlite(keyword = ""):
    start = time.perf_counter()
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    result = []
    for row in cursor.execute(
        "SELECT title from posts where content MATCH '" + keyword + "'"):
        result.append(row[0])

    end = time.perf_counter()
    return result, round(end-start,3)

result, time_spend = get_title_es("Skin")
print("ELASTICSEARCH, match_size:", len(result), " spend_time : ", time_spend, "s")

result, time_spend = get_title_sqlite(keyword = "Skin")
print("SQLITE3      , match_size:", len(result), " spend_time : ", time_spend, "s")




