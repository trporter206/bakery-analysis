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

#combine each transaction to a single row, items become list--------------------
foo = lambda a: ", ".join(a)
bakery_data['Item'].astype('category')
aggregate = {'Date': 'first', 'Time': 'first', 'Item': foo}
bakery_data = bakery_data.groupby(bakery_data['Transaction']).aggregate(aggregate)
