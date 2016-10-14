# -*- coding: utf-8 -*-
"""
Created on Tue Oct 04 16:41:13 2016
Title: Homework 2 Data Mining CSC240
@author: Hizkia
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

### Histogram for Question 3.11###
array = [13, 15, 16, 16, 19, 20, 20, 21, 22, 22, 25, 25, 25, 25, 30, 33, 33, 35,\
 35, 35, 35, 36, 40, 45, 46, 52, 70]
 
bins = np.linspace(10,100,num=10)
plt.hist(data, bins)

# Dataset used is retrieved from http://catalog.data.gov/dataset/college-scorecard
# Only the first 11 attributes were taken to reduce the size of the data set

### Question 3.13 part a ###
# Load the data set
filepath = "D://College Data.csv"
data = pd.read_csv(filepath)

# Find the number of distinct values for each attribute (column)
unique_val = []
col = data.columns
for i, item in enumerate(col):
    unique_val.append(len(data[item].unique()))

# Sort the unique values
hierarchy_idx = sorted(range(len(unique_val)), key = lambda k:unique_val[k])
print(hierarchy_idx)

# Show the hierarchy
# According to the theory, attributes in the higher levels have less distinct
# values that the ones in the lower levels
for i in hierarchy_idx:
    print(data.columns[i] + '-->')

# HCM2 = heightened cash monitoring
# STABBR = State postcode
# AccredAgency = Acreditor name
# City - City
# NPCURL = URL for institution's net price calculator
# OPEID6 = 6-digit OPE ID for institution
# INSTURL = URL for institution's homepage
# ZIP = Zip code
# INSTNM = Institution name
# OPEID = 8-digit OPE ID for institution
# UNITID = Unit ID for institution


### Question 3.13 part b ###
array = np.array([13, 15, 16, 16, 19, 20, 20, 21, 22, 22, 25, 25, 25, 25, 30, 33, 33, 35,\
 35, 35, 35, 36, 40, 45, 46, 52, 70])
# plot histogram
bins = np.linspace(10,100,num=10)
plt.figure(1)
plt.hist(array,bins)
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.title("Concept hierarchy with equal width bins")
plt.show()


### Question 3.13 part c ###
split = np.split(array,3)
plt.bar([0,1,2],[len(split[0]),len(split[1]),len(split[2])],width = 0.5)
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.title("Concept hierarchy with equal frequency")
plt.xticks([0.25,1.25,2.25], ["%d - %d"%(split[0][0],split[1][0]),"%d - %d"%(split[1][0],split[2][0]),"%d - %d"%(split[2][0],split[2][len(split)-1])])
plt.show()

