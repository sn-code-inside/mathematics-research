# load functions from packages
from pandas import read_csv

# load .csv file
df = read_csv('data/ex6-data.csv')

# print results
print('example 6 results (importing data)\n')
print('df (imported dataframe):\n',df,'\n')