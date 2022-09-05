api 주소 : py.pyeondori.kro.kr:5000

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

        main.py를 백그라운드로 실행하겠다
        => vscode 연결 종료해도 계속 실행(서버 역할)

    프로세스 종료 - kill -9 `ps -ef | grep main.py | awk '{print $2}'`

        1. ps -ef | grep main.py : 프로세스 중 main.py가 있는 것만 반환
        2. awk '{print $2}' : grep한 결과 중 2번째($2, pid) 결과만 반환

        kill -9 <pid> : 해당 pid 가진 프로세스 종료


권한이 갑자기 사라졌을 때

	1. 토큰 발행
	2. git remote set-url origin https://{토큰}@github.com/{깃허브이름}/{repost이름}.git
	3. git push


***

TODO - 2022.08.23

	프론트 엔드에서 몇 개 출력할건지 파악하여 해당 개수만큼 반환하게끔
	코드 깔끔하게 수정
	
TODO - 2022.08.26

	로그인 구현
	로그인 테스트 폼 생성

