# load functions from packages
from pandas import read_csv
from numpy import matrix

# load .csv file
df = read_csv('data/ex6-data.csv')

# convert dataframe into a data matrix
df_matrix = matrix(df)

# print results
print('example 7 results (convert data into data matrices)\n')
print('df (as a data matrix):\n',df_matrix,'\n')