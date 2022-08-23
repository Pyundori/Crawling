SQL Query 만드는 방식

1. Vender
SELECT vender, pType, pPrice, pName, pImg, gName, gPrice, gImg
FROM crawledData
{WHERE}

2. Type
SELECT * 
FROM (
	<Vender>
) <__NAME>
{WHERE}

3. Pname
SELECT * 
FROM (
	<Type>
) <__NAME>
{WHERE}

4. Price
SELECT A.vender, A.pType, A.pPrice, A.pName, A.pImg, A.gName, A.gPrice, A.gImg 
FROM (
	<Pname>
) A # <__NAME>
{WHERE}


SELECT A.vender, A.pType, A.pPrice, A.pName, A.pImg, A.gName, A.gPrice, A.gImg 
FROM (
	SELECT * 
	FROM (
		SELECT * 
		FROM (
			SELECT vender, pType, pPrice, pName, pImg, gName, gPrice, gImg
			FROM crawledData
			{WHERE}
		) <__NAME>
		{WHERE}
	) <__NAME>
	{WHERE}
) A # <__NAME>
{WHERE}