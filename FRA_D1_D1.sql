SElECT f.origin, f.des, ad.airportName, ad.lat, ad.lon, cd.cityName, ctrd.name
FROM flights AS f, airports AS ao, airports AS ad, cities AS cd, countries AS ctrd, FRA_D1
WHERE f.origin = ao.airportCode
AND f.des = ad.airportCode
AND ad.cityCode = cd.cityCode
AND ad.countryCode = cd.countryCode
AND cd.countryCode = ctrd.countryCode
AND f.origin = FRA_D1.des
AND f.httpcode = '200'
AND f.date = '2017-01-20'
ORDER BY ctrd.name