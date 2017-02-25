SELECT DISTINCT F1.origin, F2.origin AS 'transf', F2.des, ad.airportName, ad.lat, ad.lon, cd.cityName, ctrd.name
FROM flights AS F1, flights AS F2, airports AS ad, cities AS cd, countries AS ctrd
WHERE F2.des = ad.airportCode
AND ad.cityCode = cd.cityCode
AND ad.countryCode = cd.countryCode
AND cd.countryCode = ctrd.countryCode
AND F2.des NOT IN (
SELECT des
FROM FRA_D1
)
AND F1.des = F2.origin
AND F2.des != 'FRA'
AND F1.origin = 'FRA'
AND F1.httpcode = '200'
AND F2.httpcode = '200'
GROUP BY F2.des
