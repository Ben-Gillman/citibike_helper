# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 19:46:34 2018

@author: Ben
"""

import pandas as pd
from itertools import product

# Import data 
filepath = r"C:\Users\Ben\Documents\citibike_predictor\JC-201808-citibike-tripdata.csv"
df = pd.read_csv(filepath)

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

df_group = df_group.reset_index(name="bikes parked")

# Period index creation
dr = pd.date_range(min_date + " 00:00", min_date + " 23:59", freq="5min")
dr
data_placeholder = pd.DataFrame(list(product(df_group["end station name"].unique(), pd.to_datetime(dr))), 
                                 columns=("station", "time"))

# Join periodindex with dataframe to fill in null times
station_times = data_placeholder.merge(df_group, how="left", 
                                        left_on=["station", "time"], 
                                        right_on=["end station name", 
                                                      "stoptime"])

station_times = station_times.drop(columns=["end station name", "stoptime"])
station_times["bikes parked"] = station_times["bikes parked"].fillna(0)
station_times