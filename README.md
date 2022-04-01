# NoSQL-PerformanceTest
NoSQL 종류별 performance 분석을 해보자!

## Schema
### USER 정보 - Schema

|Column|Column(eng)|Description|Type|범위|
|---|---|---|---|---|
|고객 id|user_id|고객의 id|text|uuid_4|
|고객 pw|user_pw|고객의 pw|text|12자리 알파벳 + 숫자의 조합|
|고객 성명|user_name|고객의 이름|text|-|
|회원/비회원|is_member|고객이 회원인지 비회원인지?|boolean|0 = 비회원, 1 = 회원|
|성별|sex|고객의 성별|boolean|0 = 여성, 1 = 남성|
|나이|age|고객의 나이|short|12~70|
|직업|job|고객의 직업에 대한 정보|text|-|
|주소|home_address|배송이 이뤄져야할 위치에 대한 정보|text|-|

### 판매 정보 - Schema

|Column|Column(eng)|Description|Type|범위|
|---|---|---|---|---|
|고객 id|user_id|고객의 id|text|uuid_4|
|접속 IP|ip_address|ipv4|text|public ipv4|
|상품코드|product_id|어떤 상품을 구매했는지?|text|`[a-zA-Z]{1}_[0-9]{2}`, 총 5200개|
|구매개수|sell_cnt|제품을 몇개 구입했는지 조사|short|1-30|
|구매시간|sell_time|Timestamp|timestamp|2010.03.05 ~ 현재|
|구매경로|web_or_mobile|어느 경로로 구매하였는지?|text|['Web', 'Mobile']|
|구입/선물|sell_or_gift|구입 혹은 선물을 한건지?|boolean|0 = 구입, 1 = 선물|

### DB Engine 별 Test Format 

|Database|source file|
|----|----|
|RDBMS(SQLite)|csv|
|분산 KVS(DynamoDB)|csv, JSON|
|WCS(Apache Cassandra)|csv, JSON|
|Document store(MongoDB)|JSON|
|검색 엔진(ElasticSearch)|JSON|


## 결론
<https://dlgldgldgld.github.io/database/nosql/nosql_performance_test/> 참조

## Problem History

### Cassandra
- Docker에 올려서 하는건 csv import 에러가 발생.
- Local에 받아서 사용하는건 import 하는 것이 너무 느림.
- apache-cassandra-3.11.12 기준 python 2.7로 사용 가능.

실행 방법 
1. Cassandra 실행 - C:\apache\apache-cassandra-3.11.12\bin\cassandra
2. cqlsh 실행 - C:\apache\apache-cassandra-3.11.12\bin\cqlsh

