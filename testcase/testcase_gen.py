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

fake = Faker('ko_KR')
fake.add_provider(internet)

client_info = namedtuple('client_info', 
               ['user_id', 'user_name', 'is_member', 'sex', 'age', 
                'job', 'home_address', 'ip_address'])

trade_info = namedtuple('trade_info', 
              ['product_id', 'sell_cnt', 'sell_time', 'web_or_mobile', 'sell_or_gift'])

CSV_HEDAER = list(client_info._fields)
CSV_HEDAER.extend(trade_info._fields)

def gen_client() :
    for _ in range(0, 10000):
        yield client_info(
            fake.unique.uuid4(), fake.name(), fake.pybool(), fake.pybool(), fake.random.randint(12, 70),
            fake.job(), fake.unique.address(), fake.unique.ipv4_public())

def gen_loginfo( user_list, max_cnt = 100 ) :
    for _ in range(max_cnt):
        user = fake.random_element(elements = user_list)
        trade = trade_info(
                fake.bothify(text='?-##'), fake.random.randint(1, 30),
                fake.date_time_between_dates(datetime_start=STORE_OPEN_DATE, datetime_end = datetime.now()),
                fake.random_element(['Web', 'Mobile']), fake.pybool())
        yield ( user, trade )

def generate_logfile( user_list : list[(client_info, trade_info)], file_name : str, process_cnt : int , record_cnt = 10000 ) :
    loginfo = gen_loginfo(user_list, record_cnt)
    f_name = "".join([file_name, '_', str(process_cnt), '.csv'])
    with open( f_name , 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(CSV_HEDAER)

        for user, trade in loginfo :
            record = list(user)
            record.extend(trade)
            w.writerow(record)

if __name__ == "__main__" :
    filename = 'test_file_name'

    cpu_cnt = os.cpu_count()
    user_list = list(gen_client())
    per_write_record = math.ceil( ALL_RECORD_COUNT / cpu_cnt )

    with ProcessPoolExecutor() as e:
        futures = [e.submit(generate_logfile, user_list, filename, num, per_write_record) for num in range (cpu_cnt)]
        for future in as_completed(futures):
            future.result()