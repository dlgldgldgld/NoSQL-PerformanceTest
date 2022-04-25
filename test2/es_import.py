import subprocess

def delete_index(classname):
    command = "curl -XDELETE http://localhost:9200/" + classname
    subprocess.call([command], shell=True)

def import_elasticsearch(filename):
    command = "curl -XPOST http://localhost:9200/_bulk?pretty --data-binary @" + filename + " -H 'Content-Type:application/json'"
    subprocess.call([command], shell=True)

delete_index('posts')
import_elasticsearch("elastic_import.json")
