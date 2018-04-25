import pandas as pd

# Read jury data 
data = pd.read_csv('jury_data.csv', encoding= 'ISO-8859-1',skiprows=[0,2])
data.head(5)

## To describe columns
data.columns

data.describe()


# To check data type of each columns.
print(data.dtypes)


## Changing Data type
data['End Date'] = pd.to_datetime(data['End Date'])
data['Start Date'] = pd.to_datetime(data['Start Date'])
data.dtypes


import pandas as pd
df =pd.read_csv('jury2.tsv', sep='\t+', skiprows=[0, 4]+list(range(1,1614,2)) + [1614], names= range(84) )
df.head()

df = df.iloc[1:]
name_dict= { i :i for i in range(84)}
name_dict[0] = 'start_date'
name_dict[1] = 'end_date'
name_dict[2] = 'response_type'
name_dict
df.rename(index = str, columns=name_dict, inplace= True)

df.head()

df.start_date = pd.to_datetime(df.start_date)
df.dtypes
any(df.isnull().any())
# everything is nice

df.En

