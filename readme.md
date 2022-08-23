api 주소 : http://13.125.245.73:5000/

***

SQL Query 만드는 방식

```
1. Vender
SELECT *
FROM crawledData
{WHERE}
```

```
2. Type
SELECT * 
FROM (
	<Vender>
) <__NAME>
{WHERE}
```

```
3. Pname
SELECT * 
FROM (
	<Type>
) <__NAME>
{WHERE}
```

```
4. Price
SELECT A.vender, A.pType, A.pPrice, A.pName, A.pImg, A.gName, A.gPrice, A.gImg 
FROM (
	<Pname>
) A # <__NAME>
{WHERE}
```

```
SELECT A.vender, A.pType, A.pPrice, A.pName, A.pImg, A.gName, A.gPrice, A.gImg 
FROM (
	SELECT * 
	FROM (
		SELECT * 
		FROM (
			SELECT *
			FROM crawledData
			{WHERE}
		) <__NAME>
		{WHERE}
	) <__NAME>
	{WHERE}
) A # <__NAME>
{WHERE}
```

반복하면 된다.

***

nohup 사용

    프로세스 생성 - nohup python3 main.py &

    프로세스 종료 - kill -9 `ps -ef | grep main.py | awk '{print $2}'`

        1. ps -ef | grep main.py : 프로세스 중 main.py가 있는 것만 반환
        2. awk '{print $2}' : grep한 결과 중 2번째($2, pid) 결과만 반환