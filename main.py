import csv
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

bakery_data = pd.read_csv("BreadBasket_DMS.csv")

def overview(data):
    print('column names')
    print data.columns.values
    print('_'*40)
    print('column info')
    print data.info()
    print('_'*40)
    print('numeric columns')
    print data.describe()
    print('_'*40)
    print('non numeric columns')
    print data.describe(include=[np.object])

# overview(bakery_data)

#remove missing values and get basic data---------------------------------------
bakery_data = bakery_data[bakery_data.Item != "NONE"]

unique_items = bakery_data['Item'].unique()
popular_items = bakery_data.Item.value_counts()[:10]
other_items = bakery_data.Item.count() - popular_items.sum()

top_items = popular_items.append(pd.Series([other_items], index=['Others']))

print top_items

#combine each transaction to a single row, items become list--------------------
foo = lambda a: ", ".join(a).split(', ')
bakery_data['Item'].astype('category')
aggregate = {'Transaction': 'first', 'Date': 'first', 'Time': 'first', 'Item': foo}
bakery_data = bakery_data.groupby(bakery_data['Transaction']).aggregate(aggregate)


#add features-------------------------------------------------------------------
for dataset in [bakery_data]:
    dataset['Count'] = dataset['Item'].str.len()

#explore data-------------------------------------------------------------------
p = bakery_data[['Date', 'Count']].groupby('Date').sum()
p['2016-10-31': '2016-11-28'].plot()

# plt.show()
