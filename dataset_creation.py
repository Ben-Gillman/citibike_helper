# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 19:20:42 2018

@author: Ben
"""

import pandas as pd

bulk_filepath = r"C:\Users\Ben\Documents\citibike_predictor\NYC-BikeShare-2015-2017-combined.csv"
bulk_df = pd.read_csv(bulk_filepath, index_col=0)
bulk_df.describe()

# Remove junk column
bulk_df = bulk_df.drop("Trip_Duration_in_min")


