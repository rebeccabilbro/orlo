#!/usr/bin/env python
# explore.py


# Title:        Visual Exploratory Analysis
# Author:       Rebecca Bilbro
# Date:         4/4/16
# Organization: District Data Labs


#####################################################################
# Imports
#####################################################################
from sklearn.datasets import load_iris
import pandas as pd
import matplotlib.pyplot as plt
from pandas.tools.plotting import parallel_coordinates, scatter_matrix, radviz

iris   = load_iris()
df = pd.DataFrame(iris.data)
df.columns = iris.feature_names

# Boxplot
df.plot(kind='box')
plt.show()

# Histogram
df.plot(kind='hist')
plt.show()

# Radviz
df['name'] = iris.target
fig = radviz(df, 'name')
plt.show()

# Scatterplot Matrix
fig = scatter_matrix(df, alpha=0.2, diagonal='kde')
plt.show()

# Parallel Coordinates
fig = parallel_coordinates(df, 'name')
plt.show()
