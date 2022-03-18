import sqlite3
import pandas
import locale
import time
import os

table_name = "log_info"
dbname = 'example.db'

start = time.perf_counter()
conn = sqlite3.connect(dbname)
for count in range (0, 1):
    csvfile = f'test_file_name_{count}.csv'
    df = pandas.read_csv(csvfile, encoding=locale.getpreferredencoding())
    df.to_sql(table_name, conn, if_exists='append', index=False)

end = time.perf_counter()
print(f'[SQLITE3]-FILE LOADER : {end - start:0.4f} seconds')