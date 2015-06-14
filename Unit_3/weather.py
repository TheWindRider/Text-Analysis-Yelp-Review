import pandas as pd
import numpy as np
import sqlite3 as lite
import matplotlib.pyplot as plt

con = lite.connect('SQLite Data\weather.sqlite')
cur = con.cursor()

city_temperature = pd.read_sql_query("SELECT * FROM temperature", con)
city_temperature['date'] = pd.to_datetime(city_temperature['unix_time'],unit='s')
print city_temperature.groupby('city_name')['daily_max'].agg([np.mean, np.std, np.ptp])
time_temperature = city_temperature.pivot(index = 'date', columns = 'city_name', values = 'daily_max')
time_temperature[['Atlanta', 'Boston', 'San Francisco', 'Chicago', 'Seattle']].plot()
plt.show()
time_change = time_temperature.diff().abs()
city_change = time_change.sum(axis = 0)
print city_change
print city_change.describe()