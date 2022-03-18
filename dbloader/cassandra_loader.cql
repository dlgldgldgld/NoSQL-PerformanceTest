CREATE KEYSPACE IF NOT EXISTS product_sell
  WITH REPLICATION = { 
   'class' : 'SimpleStrategy',
   'replication_factor' : '3'
  };

 CREATE TABLE IF NOT EXISTS product_sell.log_info (
    user_id uuid,
    user_name text,
    is_member boolean, 
    sex boolean,
    age smallint,
    job text,
    home_address text,
    ip_address inet,
    product_id text,
    sell_cnt smallint,
    sell_time timestamp,
    web_or_mobile text,
    sell_or_gift boolean,
    PRIMARY KEY (user_id)
);

CREATE TABLE IF NOT EXISTS product_sell.abc (
    user_id text,
    user_name text,
    is_member boolean, 
    sex boolean,
    age smallint,
    job text,
    home_address text,
    ip_address inet,
    product_id text,
    sell_cnt smallint,
    sell_time timestamp,
    web_or_mobile text,
    sell_or_gift boolean,
    PRIMARY KEY (user_id)
);

# table clear
TRUNCATE product_sell.abc; 

# insert csv file
COPY product_sell.abc (user_id, user_name, is_member, sex, age, job, home_address, ip_address, product_id, sell_cnt, sell_time, web_or_mobile, sell_or_gift) 
FROM 'D:/01.Develop/02.PYTHON/08.NoSQL-PerformanceTest/input/test_file_name_0.csv' WITH HEADER = TRUE AND DELIMITER = ',' AND MINBATCHSIZE=50 AND MAXBATCHSIZE=100;

COPY product_sell.log_info (user_id, user_name, is_member, sex, age, job, home_address, ip_address, product_id, sell_cnt, sell_time, web_or_mobile, sell_or_gift) 
FROM 'D:/01.Develop/02.PYTHON/08.NoSQL-PerformanceTest/input/test_file_name_0.csv' WITH DELIMITER = ',';

COPY product_sell.log_info (user_id, user_name, is_member, sex, age, job, home_address, ip_address, product_id, sell_cnt, sell_time, web_or_mobile, sell_or_gift) 
FROM '../input/test_file_name_1.csv' WITH HEADER = TRUE;

COPY product_sell.log_info (user_id, user_name, is_member, sex, age, job, home_address, ip_address, product_id, sell_cnt, sell_time, web_or_mobile, sell_or_gift) 
FROM '../input/test_file_name_2.csv' WITH HEADER = TRUE;

COPY product_sell.log_info (user_id, user_name, is_member, sex, age, job, home_address, ip_address, product_id, sell_cnt, sell_time, web_or_mobile, sell_or_gift) 
FROM '../input/test_file_name_3.csv' WITH HEADER = TRUE;

COPY product_sell.log_info (user_id, user_name, is_member, sex, age, job, home_address, ip_address, product_id, sell_cnt, sell_time, web_or_mobile, sell_or_gift) 
FROM '../input/test_file_name_4.csv' WITH HEADER = TRUE;

COPY product_sell.log_info (user_id, user_name, is_member, sex, age, job, home_address, ip_address, product_id, sell_cnt, sell_time, web_or_mobile, sell_or_gift) 
FROM '../input/test_file_name_5.csv' WITH HEADER = TRUE;