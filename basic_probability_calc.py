# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 19:46:34 2018

@author: Ben
"""

import pandas as pd

filepath = r"C:\Users\Ben\Documents\citibike_predictor\JC-201808-citibike-tripdata.csv"
df = pd.read_csv(filepath)

df.dtypes
df

# Convert times from objects to datetimes
df["startdatetime"] = pd.to_datetime(df["starttime"])
df["stopdatetime"] = pd.to_datetime(df["stoptime"])

# Get times from datetimes 
min_date = (pd.Timestamp.min + pd.DateOffset(1)).strftime("%Y-%m-%d")
df["starttime"] = pd.to_datetime(min_date + " " + df["startdatetime"].apply(lambda x: x.strftime("%H:%M:%S")))
df["stoptime"] = pd.to_datetime(min_date + " " + df["stopdatetime"].apply(lambda x: x.strftime("%H:%M:%S")))

# Get weekday vs weekend tag

# Break out into 5 min buckets
df.set_index('stoptime', inplace=True)
grouper = pd.Grouper(freq='5Min')
df_group = (df.groupby([df['end station name'], grouper])
              ['end station name']
              .agg('count'))

# Period index creation
dr = pd.date_range("00:00", "23:59", freq="5min").time
px = pd.PeriodIndex(start="00:00", end="23:59", freq="5min")
px
