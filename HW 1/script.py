# Importing pandas library
from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Filepath to IRIS dataset
path = "https://raw.githubusercontent.com/hizkiafebianto/CSC240/master/iris.data"

# Reading IRIS data set and create a Data Frame, called irisraw
header = ['sepal_l', 'sepal_w','petal_l','petal_w','type']
irisraw = pd.read_csv(path, header = None, names = header)

# Summary statistics for each attribute
print(irisraw.describe())

# Separate data based on type
irisSetosa = irisraw[irisraw.type == 'Iris-setosa']
irisVersicolor = irisraw[irisraw.type == 'Iris-versicolor']
irisVirginica = irisraw[irisraw.type == 'Iris-virginica']
irisVersicolor.index = range(50)
irisVirginica.index = range(50)

print(irisSetosa.describe())
print(irisVirginica.describe())
print(irisVersicolor.describe())

# Distribution of petal length
plt.hist(irisSetosa.petal_l)
plt.hist(irisVersicolor.petal_l)
plt.hist(irisVirginica.petal_l)
plt.legend(['Setosa','Versicolor','Virginica'])
plt.title("Petal Length Distribution")
plt.show()

# Distribution of petal width
plt.hist(irisSetosa.petal_w)
plt.hist(irisVersicolor.petal_w)
plt.hist(irisVirginica.petal_w)
plt.legend(['Setosa','Versicolor','Virginica'])
plt.title("Petal Width Distribution")
plt.show()

# Distribution of sepal length
plt.hist(irisSetosa.sepal_l)
plt.hist(irisVersicolor.sepal_l)
plt.hist(irisVirginica.sepal_l)
plt.legend(['Setosa','Versicolor','Virginica'])
plt.title("Sepal Length Distribution")
plt.show()

# Distribution of sepal width
plt.hist(irisSetosa.sepal_w)
plt.hist(irisVersicolor.sepal_w)
plt.hist(irisVirginica.sepal_w)
plt.legend(['Setosa','Versicolor','Virginica'])
plt.title("Sepal Width Distribution")
plt.show()


plt.scatter(irisSetosa.petal_l,irisSetosa.petal_w, c = 'red')
plt.scatter(irisVersicolor.petal_l,irisVersicolor.petal_w, c = 'blue')
plt.scatter(irisVirginica.petal_l,irisVirginica.petal_w, c = "yellow")
plt.legend(['Setosa','Versicolor','Virginica'], loc = 4)
plt.ylabel("Petal Width (cm)")
plt.xlabel("Petal Length (cm)")
plt.title("Petal Distribution")
plt.show()

plt.scatter(irisSetosa.sepal_l,irisSetosa.sepal_w, c = 'red')
plt.scatter(irisVersicolor.sepal_l,irisVersicolor.sepal_w, c = 'blue')
plt.scatter(irisVirginica.sepal_l,irisVirginica.sepal_w, c = "yellow")
plt.legend(['Setosa','Versicolor','Virginica'], loc = 4)
plt.ylabel("Sepal Width (cm)")
plt.xlabel("Sepal Length (cm)")
plt.title("Sepal Distribution")
plt.show()




