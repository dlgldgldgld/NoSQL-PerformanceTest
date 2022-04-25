import os
import subprocess
import time

def sqlite_import( db_file, table_schema, csv_file ) :
    if os.path.exists(db_file) :
        os.remove(db_file)
    
    create_table = subprocess.Popen(['sqlite3', db_file, table_schema])
    create_table.communicate()

    import_csv = subprocess.Popen(['sqlite3', db_file], stdin = subprocess.PIPE, stdout=subprocess.PIPE)
    import_csv.stdin.write(bytes('.separator ,\n', 'utf-8'))
    import_csv.stdin.write(bytes('.import ' + csv_file + ' posts\n', 'utf-8'))

    start = time.perf_counter()
    import_csv.communicate()
    end = time.perf_counter()

    return round(end-start,3)

sqlite_import("example.db", "CREATE VIRTUAL TABLE posts using fts5(title,content);", "fts_import.csv")
