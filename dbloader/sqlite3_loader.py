import sqlite3
import pandas
import locale
import time
import os

table_name = "log_info"
dbname = 'example.db'

start = time.perf_counter()
if os.path.exists(dbname) :
    os.remove(dbname)
conn = sqlite3.connect(dbname)

conn.execute("""
CREATE TABLE [log_info](
  [user_id] TEXT PRIMARY KEY, 
  [user_pw] TEXT, 
  [user_name] TEXT, 
  [is_member] INTEGER, 
  [sex] INTEGER, 
  [age] INTEGER, 
  [job] TEXT, 
  [home_address] TEXT, 
  [ip_address] TEXT);
""")

for count in range (0, 1):
    csvfile = f'test_file_name_{count}.csv'
    df = pandas.read_csv(csvfile, encoding=locale.getpreferredencoding())
    df.to_sql(table_name, conn, if_exists='append', index=False)

conn.close()
end = time.perf_counter()
print(f'[SQLITE3]-FILE LOADER : {end - start:0.4f} seconds')