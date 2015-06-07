# New Yorkers Bike
import requests
from pandas.io.json import json_normalize
from dateutil.parser import parse
import sqlite3 as lite
import time
import collections

raw_data = requests.get('http://www.citibikenyc.com/stations/json')
bike_station = json_normalize(raw_data.json()['stationBeanList'])
station_ids = bike_station['id'].tolist()
station_ids = ['_' + str(x) + ' INT' for x in station_ids]
"""
print bike_station['testStation'].describe()
print bike_station['statusValue'].describe()
print bike_station['totalDocks'].describe()
condition = bike_station['statusValue'] == 'In Service'
print bike_station[condition]['totalDocks'].describe()
"""
con = lite.connect('SQLite Data\citi_bike.sqlite')
cur = con.cursor()
sql_create_ref = "CREATE TABLE citibike_reference (id INT PRIMARY KEY, totalDocks INT, city TEXT, altitude INT, stAddress2 TEXT, longitude NUMERIC, postalCode TEXT, testStation TEXT, stAddress1 TEXT, stationName TEXT, landMark TEXT, latitude NUMERIC, location TEXT )"
sql_insert_ref = "INSERT INTO citibike_reference (id, totalDocks, city, altitude, stAddress2, longitude, postalCode, testStation, stAddress1, stationName, landMark, latitude, location) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)"
sql_create_act = "CREATE TABLE available_bikes ( execution_time TEXT, " +  ", ".join(station_ids) + ");"
with con: 
    cur.execute(sql_create_ref)
    cur.execute(sql_create_act)
    for index, station in bike_station.iterrows():
        cur.execute(sql_insert_ref,(station['id'],station['totalDocks'],station['city'],station['altitude'],station['stAddress2'],station['longitude'],station['postalCode'],station['testStation'],station['stAddress1'],station['stationName'],station['landMark'],station['latitude'],station['location']))

for i in range(60): 
    raw_data = requests.get('http://www.citibikenyc.com/stations/json')
    bike_station = json_normalize(raw_data.json()['stationBeanList'])
    id_bikes = collections.defaultdict(int)
    exec_time = parse(raw_data.json()['executionTime'])
    print exec_time
    for index, station in bike_station.iterrows():
        id_bikes[station['id']] = station['availableBikes']
    sql_insert_act = "INSERT INTO available_bikes (execution_time) VALUES (?)"
    with con: 
        cur.execute(sql_insert_act, (exec_time.strftime('%c'),))
        for k, v in id_bikes.iteritems():
            sql_update_station = "UPDATE available_bikes SET _" + str(k) + " = " + str(v) + " WHERE execution_time = '" + exec_time.strftime('%c') + "';"
            cur.execute(sql_update_station)
    time.sleep(60)
