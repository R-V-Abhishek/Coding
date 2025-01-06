# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 20:01:49 2023

@author: Manoj
"""

import pandas as pd

# Update the file name to match the actual file in your workspace
drinks = pd.read_csv(r'C:\Users\rvabh\OneDrive\Desktop\Coding\Python for Data Science\alcohol-consumption.csv')

# examine the data's first five rows
print(drinks.head())

print(drinks['country'].describe())
#print(drinks['continent'].describe())
print(drinks['beer_percentage'].describe())

#print(drinks['beer_servings'].describe())