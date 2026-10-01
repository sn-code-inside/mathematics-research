# load functions from packages
from pandas import read_csv
from numpy import matrix

# load .csv file
df = read_csv('data/ex6-data.csv')

# form dataframe into long (stacking columns into one)
df_long = df.melt(ignore_index=False,
                  var_name='column',value_name='value')

# form dataframe into wide (rearranging the stacked columns back)
df_wide = df_long.pivot(columns='column', values='value')

# print results
print('example 9 results (shapeforming dataframes)\n')
print('df with',df.shape,'shape:\n',df,'\n')
print('df_long with',df_long.shape,'shape:\n',df_long,'\n')
print('df_wide with',df_wide.shape,'shape:\n',df_wide,'\n')