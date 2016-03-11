db_prefix = {
    209 : '209',
    210 : '210',
    211 : '211',
    212 : '212',
    213 : '213',
    214 : '214',
    215 : '215',
    216 : '216',
    217 : '217',
    218 : '219'}

import mysql.connector

connectionString = 
components = connectionString.split("@")

auth = components[0].split(":")
hostdb = components[1].split("/")

config = {
            'user': auth[0],
            'password': auth[1],
            'host': hostdb[0],
            'database': hostdb[1],
            'raise_on_warnings': True,
        }

con = mysql.connector.connect(**config)
cur = con.cursor(dictionary=True)

data = []

for key, value in db_prefix.items():
    try:
        cur.execute("SELECT * FROM "+ value +"_offspring")
        results = cur.fetchall()
        for r in results:
            r['Exp_Num'] = key
            data.append(r)
    except:
        continue

cur.close()
con.close()

import json
json.dump(data,open('offspring.json','w'))

