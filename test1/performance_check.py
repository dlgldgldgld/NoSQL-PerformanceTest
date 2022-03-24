from collections import namedtuple

import re
import os
import subprocess
import time
import matplotlib.pyplot as plt
from pyparsing import empty

fn_sqlite = 'test1.db'
fp_sqlite = 'sqlite3'
fn_testcsv = 'test_file_name_1.csv'

time_rec = namedtuple('time_rec', ['case', 'time'])
time_spent = dict()

tc_query_index = " \
CREATE TABLE [log_info]( \
  [user_id] TEXT PRIMARY KEY, \
  [user_pw] TEXT, \
  [user_name] TEXT, \
  [is_member] INTEGER, \
  [sex] INTEGER, \
  [age] INTEGER, \
  [job] TEXT, \
  [home_address] TEXT, \
  [ip_address] TEXT);"

tc_query_no_index = " \
CREATE TABLE [log_info]( \
  [user_id] TEXT, \
  [user_pw] TEXT, \
  [user_name] TEXT, \
  [is_member] INTEGER, \
  [sex] INTEGER, \
  [age] INTEGER, \
  [job] TEXT, \
  [home_address] TEXT, \
  [ip_address] TEXT);"


def sqlite_import_test( db_file, table_schema, csv_file ) :
    if os.path.exists(db_file) :
        os.remove(db_file)
    create_table = subprocess.Popen([fp_sqlite, db_file, table_schema])
    create_table.communicate()

    import_csv = subprocess.Popen([fp_sqlite, db_file], stdin = subprocess.PIPE, stdout=subprocess.PIPE)
    import_csv.stdin.write(bytes('.separator ,\n', 'utf-8'))
    import_csv.stdin.write(bytes('.import ' + csv_file + ' log_info\n', 'utf-8'))

    start = time.perf_counter()
    import_csv.communicate()
    end = time.perf_counter()

    return round(end-start,3)

def show_graph(labels, sqlite_means, sqlite_idx_means ,cassandra_means):
    import numpy as np
    x_len = len(labels)
    x = np.arange(x_len)  # the label locations
    width = 0.2  # the width of the bars
    fig, ax = plt.subplots()
    rects1 = ax.bar(x-(width/2)*(x_len-1), sqlite_means, width, label='sqlite_no_index')
    rects2 = ax.bar(x, sqlite_idx_means, width, label='sqlite_index')
    rects3 = ax.bar(x+(width/2)*(x_len-1), cassandra_means, width, label='cassandra')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('seconds')
    ax.set_title('CSV import result')
    ax.set_xticks(x, labels)
    ax.legend()

    ax.bar_label(rects1, padding=1)
    ax.bar_label(rects2, padding=1)
    ax.bar_label(rects3, padding=1)

    fig.tight_layout()
    plt.show()

def cassandra_import_test(csv_file):
    truncate_tbl = subprocess.Popen(['cqlsh.bat'], stdin=subprocess.PIPE)
    truncate_tbl.stdin.write(bytes("truncate product_sell.client_info;", 'utf-8'))
    truncate_tbl.communicate()
    
    cassandra_query = "COPY product_sell.client_info (user_id, user_pw, user_name, is_member, sex, age, job, home_address, ip_address)" + \
        " FROM " + "'" +csv_file + "'" + " WITH HEADER = TRUE AND DELIMITER = ',';"

    import_csv = subprocess.Popen(['cqlsh.bat'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    import_csv.stdin.write(bytes(cassandra_query, 'utf-8'))
    cql_res, _ = import_csv.communicate()

    contents = cql_res.split(b'\n')
    t_info = [c.decode('utf-8') for c in contents if b'imported' in c]
    print(t_info[0])
    
    seconds = re.compile('[0-9]+\.[0-9]+ seconds').search(t_info[0]).group()
    if (minutes := re.compile('[0-9]+ minute').search(t_info[0])) is not None:
        minutes = float(minutes.group().split(sep=' ')[0])
    else :
        minutes = 0.0

    seconds = float(seconds.split(sep=' ')[0])
    return float(minutes*60+seconds)

if __name__ == "__main__" :
    labels = ['1000000 rows', '5000000 rows', '10000000 rows']
    csv_files = ['1000000.csv', '5000000.csv', '10000000.csv']
    sqlite_means = []
    sqlite_idx_means = []
    cassandra_means = []

    for csv_file in csv_files :
        sqlite_idx_means.append(sqlite_import_test('test1.db', tc_query_index, csv_file))
        sqlite_means.append(sqlite_import_test('test2.db', tc_query_no_index, csv_file))
        cassandra_means.append(cassandra_import_test(csv_file))

    print(f'{sqlite_means=}, {sqlite_idx_means=}, {cassandra_means=}')    
    show_graph(labels, sqlite_means, sqlite_idx_means, cassandra_means)