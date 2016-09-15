# Importing pandas library
from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import os
#import matplotlib.pyplot as plt

# Filepath to IRIS dataset
path = os.getcwd() + '\iris.data'

# Reading IRIS data set and create a Data Frame, called irisraw
header = ['sepal_l', 'sepal_w','petal_l','petal_w','type']
irisraw = pd.read_csv(path, header = None, names = header)

# Summary statistics for each attribute
#print(irisraw.describe())

# Separate data based on type
irisSetosa = irisraw[irisraw.type == 'Iris-setosa']
irisVersicolor = irisraw[irisraw.type == 'Iris-versicolor']
irisVirginica = irisraw[irisraw.type == 'Iris-virginica']

#print(irisSetosa.describe())
#print(irisVirginica.describe())
#print(irisVersicolor.describe())

np.histogram(irisSetosa.sepal_l, bins = 1)

#print(irisVirginica)
