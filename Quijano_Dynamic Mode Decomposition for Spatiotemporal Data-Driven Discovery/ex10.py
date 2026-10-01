# load functions from packages
from pandas import DataFrame, concat

# create custom datasets
data = {'col1': [0,1,2,3,4],
        'col2': [1,1,2,3,5],
        'col3': [1,1,4,6,20]}

# create dataframes using the defined data
df = DataFrame(data)

# accessing columns
col1 = df['col1'] # accessing 'col1' of df_1 dataframe

# create a new column then add into existing dataframe
df['col4'] = [2,3,8,12,29]

# create new rows then add into existing dataframe
new_data = {'col1': [5,6],
            'col2': [7,12],
            'col3': [12,18],
            'col4': [24,36]}
new_df = DataFrame(new_data)
df = concat([df,new_df], ignore_index=True)

# export dataframe into .csv file
df.to_csv('data/ex10-data.csv')

# print results
print('example 10 (manipulating and exporting dataframes)\n')
print('df:\n',df,'\n')
print('data saved to data/ex10-data.csv')