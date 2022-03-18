from collections import namedtuple
from faker import Faker
from faker.providers import internet
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor, as_completed

import math
import os
import csv

STORE_OPEN_DATE = datetime(2010, 3, 5)
ALL_RECORD_COUNT = 10000000

fake = Faker()
fake.add_provider(internet)

client_info = namedtuple(
    'client_info', ['user_id', 'user_pw', 
    'user_name', 'is_member', 'sex', 
    'age', 'job', 'home_address', 'ip_address'])

trade_info = namedtuple(
    'trade_info', ['product_id', 'sell_cnt', 
    'sell_time', 'web_or_mobile', 'sell_or_gift'])

CSV_HEADER = list(client_info._fields)
CSV_HEADER.extend(trade_info._fields)

def gen_client( user_cnt = 10000 ) :
    for _ in range(0, user_cnt):
        address = fake.unique.address()
        address = address.replace("\n", " ")
        yield client_info(
            fake.unique.uuid4(), fake.password(length=12, upper_case=True), fake.name(), 
            fake.pybool(), fake.pybool(), fake.random.randint(12, 70),
            fake.job(), address, fake.unique.ipv4_public())

def gen_loginfo( user_list, max_cnt = 100 ) :
    for _ in range(max_cnt):
        user = fake.random_element(elements = user_list)
        trade = trade_info(
                fake.bothify(text='?-##'), fake.random.randint(1, 30),
                fake.date_time_between_dates(datetime_start=STORE_OPEN_DATE, datetime_end = datetime.now()),
                fake.random_element(['Web', 'Mobile']), fake.pybool())
        yield ( user, trade )

def generate_clientfile( 
    process_cnt : int, record_cnt : int, 
    file_name :str, header : list[str] ):
    """generate client information to csv file.

    Args:
        process_cnt (int): if this function will be executed by multiprocess, using this args for distinguishing process number.
        file_name (_type_): result file name
        header (list[str]): result csv file header list.
        record_cnt (int): records count.
    """
    generator = gen_client(record_cnt)
    outfilename = "".join([file_name, "_", str(process_cnt), ".csv"])
    with open( outfilename, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(header)
        for client in generator:
            w.writerow(client)

def generate_logfile( 
    process_cnt : int, record_cnt : int,
    file_name : str, header : list[str], user_list : list[client_info]) :
    """Generate combine user_info with trade_info. and It will convert to CSV file.

    Args:
        process_cnt (int): if this function will be executed by multiprocess, using this args for distinguishing process number.
        user_list (list[client_info]): user_information
        file_name (str): csv file name
        header (list[str]): csv file header
        record_cnt (int, optional): log file records count. Defaults to 10000.
    """
    loginfo = gen_loginfo(user_list, record_cnt)
    f_name = "".join([file_name, '_', str(process_cnt), '.csv'])
    with open( f_name , 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(header)

        for user, trade in loginfo :
            record = list(user)
            record.extend(trade)
            w.writerow(record)

def multiprocess_start( f , *args ) :
    cpu_cnt = os.cpu_count()
    per_write_record = math.ceil( ALL_RECORD_COUNT / cpu_cnt )

    with ProcessPoolExecutor() as e:
        futures = [e.submit(f, num, per_write_record, *args ) for num in range (cpu_cnt)]
        for future in as_completed(futures):
            future.result()

if __name__ == "__main__" :
    filename = 'test_file_name'
    # client info
    generate_clientfile(0, ALL_RECORD_COUNT, filename, list(client_info._fields) )
    # log info
    # user_list = list(gen_client())
    # multiprocess_start( generate_logfile, filename, CSV_HEADER, user_list )