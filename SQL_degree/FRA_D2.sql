SELECT DISTINCT des, airportName, lat, lon, cityName, name
FROM FRA_D1_D1_Net
WHERE FRA_D1_D1_Net.des NOT IN (
	SELECT FRA_D1.des
	FROM FRA_D1
)