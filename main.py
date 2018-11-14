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
values = top_items.tolist()
labels = popular_items.index.values.tolist()
orders_w_coffee = bakery_data[bakery_data['Item'] == 'Coffee']['Transaction'].tolist()

#df with only orders including coffee
bakery_copy = bakery_data
bakery_copy = bakery_copy[bakery_copy['Transaction'].isin(orders_w_coffee)]

pop_items_w_coffee = bakery_copy.Item.value_counts()[:10]
popular_items = bakery_data.Item.value_counts()[:10]

pop_items_w_coffee = pop_items_w_coffee.drop(labels=['Coffee'])
popular_items = popular_items.drop(labels=['Coffee'])
print pop_items_w_coffee
#item names
labels = pop_items_w_coffee.index.values.tolist()

vals_coffee = pop_items_w_coffee.tolist()
vals = popular_items.tolist()
vals_wo_coffee = [vals[i] - v for i,v in enumerate(vals_coffee)]

#df showing how often items are/not ordered with coffee
coffee_df = pd.DataFrame({'Item': pd.Series(labels), 'with_coffee': vals_coffee, 'without_coffee': vals_wo_coffee})

#add features
for dataset in [coffee_df]:
    dataset['ratio_w_coffee'] = dataset['with_coffee'] / dataset['without_coffee']
    dataset['perc_of_coffee'] = (dataset['with_coffee'] / 5471)*100
print coffee_df
# #combine each transaction to a single row, items become list--------------------
# foo = lambda a: ", ".join(a).split(', ')
# bakery_data['Item'].astype('category')
# aggregate = {'Transaction': 'first', 'Date': 'first', 'Time': 'first', 'Item': foo}
# bakery_data = bakery_data.groupby(bakery_data['Transaction']).aggregate(aggregate)
#
#
# #add features-------------------------------------------------------------------
# for dataset in [bakery_data]:
#     dataset['Count'] = dataset['Item'].str.len()
#
# #explorations-------------------------------------------------------------------
# p = bakery_data[['Date', 'Count']].groupby('Date').sum()
# p['2016-10-31': '2016-11-28'].plot()

# plt.show()
