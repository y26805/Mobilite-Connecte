SELECT DISTINCT F1.origin, F2.origin AS 'transf', F2.des
FROM flights AS F1, flights AS F2
WHERE F2.des NOT IN (
SELECT des
FROM FRA_D1
)
AND F1.des = F2.origin 
AND F2.des != 'FRA'
AND F1.origin = 'FRA'
AND F1.httpcode = '200'
AND F2.httpcode = '200'
AND F1.date = '2017-01-20'
AND F2.date = '2017-01-20'
GROUP BY F2.des