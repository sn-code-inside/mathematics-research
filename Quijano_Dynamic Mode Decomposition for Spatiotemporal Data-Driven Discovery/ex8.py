# load functions from packages
from pandas import read_csv
from numpy import matrix

# load .csv file
df = read_csv('data/ex6-data.csv')

# convert dataframe into a data matrix
df_matrix = matrix(df)

# arrange data into X and X'
m = df_matrix.shape[1] # get number of columns
X = df_matrix[:,0:m-1] # access columns 1 to m-1
X_prime = df_matrix[:,1:m] # access columns 2 to m

# print results
print('example 8 results (rearranging data matrices)\n')
print('X:\n',X,'\n')
print('X_prime:\n',X_prime,'\n')