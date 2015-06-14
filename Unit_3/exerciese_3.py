"""
# New Yorkers Bike
import time
import requests
from dateutil.parser import parse
import collections
import sqlite3 as lite

con = lite.connect('SQLite Data\citi_bike.sqlite')
cur = con.cursor()

for i in range(60):
    r = requests.get('http://www.citibikenyc.com/stations/json')
    exec_time = parse(r.json()['executionTime'])

    cur.execute('INSERT INTO available_bikes (execution_time) VALUES (?)', (exec_time.strftime('%c'),))
    con.commit()
    
    id_bikes = collections.defaultdict(int)
    for station in r.json()['stationBeanList']:
        id_bikes[station['id']] = station['availableBikes']

    for k, v in id_bikes.iteritems():
        cur.execute("UPDATE available_bikes SET _" + str(k) + " = " + str(v) + " WHERE execution_time = '" + exec_time.strftime('%c') + "';")
    con.commit()

    time.sleep(60)
con.close()
"""
# Weather
import time
import datetime
import requests
import sqlite3 as lite

APIKEY = 'bd9195a276f48c072b0689a15f7910e6'
datetime_now = datetime.datetime.now()
unix_now = int(time.mktime(datetime_now.timetuple()))
url_example = 'https://api.forecast.io/forecast/' + APIKEY + '/37.727239,-123.032229,' + str(unix_now)
data_example = requests.get(url_example)
print data_example.json().keys()
print data_example.json()['daily']['data'][0].keys()

cities = {
"Atlanta": '33.762909,-84.422675', 
"Austin": '30.303936,-97.754355', 
"Boston": '42.331960,-71.020173', 
"Chicago": '41.837551,-87.681844', 
"Cleveland": '41.478462,-81.679435', 
"Denver": '39.761850,-104.881105', 
"Las Vegas": '36.229214,-115.26008', 
"Los Angeles": '34.019394,-118.410825', 
"Miami": '25.775163,-80.208615', 
"Minneapolis": '44.963324,-93.268320', 
"Nashville": '36.171800,-86.785002', 
"New Orleans": '30.053420,-89.934502', 
"New York": '40.663619,-73.938589', 
"Philadelphia": '40.009376,-75.133346', 
"Phoenix": '33.572154,-112.090132', 
"Salt Lake City": '40.778996,-111.932630', 
"San Francisco": '37.727239,-123.032229', 
"Seattle": '47.620499,-122.350876', 
"Washington": '38.904103,-77.017229'
}

con = lite.connect('SQLite Data\weather.sqlite')
cur = con.cursor()
with con: 
    for i in range(31): 
        unix_curr = int(time.mktime((datetime_now - datetime.timedelta(days=i)).timetuple()))
        for k, v in cities.iteritems(): 
            url_curr = 'https://api.forecast.io/forecast/' + APIKEY + '/' + v + ',' + str(unix_curr)
            raw_data = requests.get(url_curr)
            daily_max = raw_data.json()['daily']['data'][0]['temperatureMax']
            sql_insert = "INSERT INTO temperature (unix_time, city_name, daily_max) VALUES (?,?,?)"
            cur.execute(sql_insert, (unix_curr, k, daily_max))
