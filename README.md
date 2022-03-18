# NoSQL-PerformanceTest
NoSQL 종류별 performance 분석을 해보자!

## TestCase 추출
일단 NoSQL 별로 Test 측정을 해볼 데이터 Set부터 설계해보자.  
첫째로는 Key-Value의 장점을 확인하기 위한 유저 정보 list에 대해서 Schema를 구성해보자.

Schema는 아래와 같이 정해보았다.

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

그리고 웹 서비스를 통해 상품을 판매하고 있다는 것을 가정하여 판매 정보에 대해서도 미리 Schema를 정해두자.

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

다음으로는 NoSQL의 종류별로 Test 가능한 Source 파일을 정해보자.
csv, json을 사용할 예정이며 사용해볼 소스파일의 format은 다음과 같이 정하였다.

|Database|source file|
|----|----|
|RDBMS(SQLite)|csv|
|분산 KVS(DynamoDB)|csv, JSON|
|WCS(Apache Cassandra)|csv, JSON|
|Document store(MongoDB)|JSON|
|검색 엔진(ElasticSearch)|JSON|

**TEST 1. RDBMS vs WCS 비교 - 유저 정보 Read / Write 시간 비교**
처음으로 해볼 것은 RDBMS와 WCS를 비교해본다.  
좀 더 엄밀히 말하자면 Key-Value Store와 RDBMS 사이에 어떠한 차이가 있는지에 대해서 비교를 해보고자 한다.

실시간 웹 서비스에서 유저의 정보를 빠르게 받아오고 가져오는 상황이 일어났다고 하자.  
첫번째로 알아보고 싶은 것은 실제 Write 속도가 얼마나 차이가 있을지에 대한 차이다.  

아래의 테스트 환경으로 진행해보자.

**Environments**
- RDBMS = SQLITE3( Local ), WCS = Cassandra( Local )
  - 서비스를 진행 중인 상태를 가정할 것이기 때문에 SQLITE3에서는 Index를 미리 만들어 놓기로 한다. ( Write 속도는 느려지나, Read 속도는 빨라짐 )
- 약 500만 명의 유저정보가 있다고 가정하고 해당 정보를 각 DB에 저장.
- 유저정보에 관한 Schema는 위에서 정의한 Schema와 동일.
- Primary Key는 user_id 이다.

<br>

**TEST 1. RESULT**

|Case|소요시간(sec)|
|----|----|
|SQLITE3 Write(No Index)|39.6116 seconds|
|SQLITE3 Write(Index)|165.6336 seconds|
|CASSANDRA Write(Optimizer)|113.722 seconds|


**TEST 2. Requirement**
 - 현재 마켓의 고객은 총 10,000명으로 가정.
 - 마켓의 Open 날짜는 2010년 3월 5일로 구매 시간은 2010.03.05 ~ 현재까지로 구성.
 - 총 1,000 만개의 record 생성.
 - 고객 성명은 중복될 수 있음.

<br> 

## Problem History

### Cassandra
- Docker에 올려서 하는건 csv import 에러가 발생.
- Local에 받아서 사용하는건 import 하는 것이 너무 느림.
- apache-cassandra-3.11.12 기준 python 2.7로 사용 가능.

실행 방법 
1. Cassandra 실행 - C:\apache\apache-cassandra-3.11.12\bin\cassandra
2. cqlsh 실행 - C:\apache\apache-cassandra-3.11.12\bin\cqlsh