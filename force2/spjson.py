import sqlite3
import json
import collections

conn = sqlite3.connect('../../Mobilite-Connecte/mobility.db')
cur = conn.cursor()

print("Creating JSON output on spider.js...")

cur.execute('''
SELECT t.airportCode, COUNT(flights.des) AS count, t.airportName, t.name AS country
FROM (SELECT a.airportCode, a.airportName, c.name
FROM airports AS a, EUplus AS e, countries AS c
WHERE a.countryCode = e.Code AND c.countryCode = e.Code) AS t
LEFT JOIN flights ON t.airportCode = flights.origin AND flights.httpcode = '200'
GROUP BY t.airportCode
ORDER BY count DESC
''')

rows = cur.fetchall()

nodes = []
count = 1
r1 = range(0,51)
r2 = range(51,101)
r3 = range(101,151)
r4 = range(151,300)

for row in rows:
    count = count + 1
    rank = 0
    if count in r1:
        rank = 0
    if count in r2:
        rank = 1
    if count in r3:
        rank = 2
    if count in r4:
        rank = 3
    obj = {
        'id' : row[0],
        'num' : row[1],
        'group' : rank,
        'name' : row[2],
        'country' : row[3]
    }
    nodes.append(obj)


cur.execute('''SELECT DISTINCT origin, des
FROM flights
WHERE httpcode = '200'
''')

rows = cur.fetchall()

links = []

for row in rows:
    obj = {
        'source' : row[0],
        'target' : row[1],
        'value' : 3
    }
    links.append(obj)

lst = {
    'nodes' : nodes,
    'links' : links
}

with open('spider2.json', 'w') as outfile:
    json.dump(lst, outfile)

print("Export done")
