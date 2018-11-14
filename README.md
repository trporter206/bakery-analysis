# Bakery Transactions Analysis

This is a simple analysis of a dataset containing 6000 transactions from a bakery. Columns include Date, Time, Transaction, and Item. The dataset was provided by Kaggle

## Questions

I started by thinking of questions one might ask when exploring transactions from a shop. This gives me an idea of what direction I should go with my code

 - What days are the busiest?
 - How many items are bought on average?
 - What are the most popular items?
 - What are the most popular pairings?

## Code Overview

### Preview

After importing the necessary libraries and reading the file to get started, I first made a function combining pandas DataFrame functions to give a detailed summary of the data.

~~~~python
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
~~~~

This is our initial result:
~~~~
column names
['Date' 'Time' 'Transaction' 'Item']
________________________________________
column info
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 21293 entries, 0 to 21292
Data columns (total 4 columns):
Date           21293 non-null object
Time           21293 non-null object
Transaction    21293 non-null int64
Item           21293 non-null object
dtypes: int64(1), object(3)
memory usage: 665.5+ KB
None
________________________________________
numeric columns
        Transaction
count  21293.000000
mean    4951.990889
std     2787.758400
min        1.000000
25%     2548.000000
50%     5067.000000
75%     7329.000000
max     9684.000000
________________________________________
non numeric columns
              Date      Time    Item
count        21293     21293   21293
unique         159      8240      95
top     2017-02-04  12:07:39  Coffee
freq           302        16    5471
~~~~

An interesting detail is that there are about 21000 rows, even though there are 6000 transactions. This tells us that the data is organized in a way such that a single transaction takes multiple rows. `bakery_data.head()` confirms this.

~~~~
Date      Time  Transaction           Item
0  2016-10-30  09:58:11            1          Bread
1  2016-10-30  10:05:34            2   Scandinavian
2  2016-10-30  10:05:34            2   Scandinavian
3  2016-10-30  10:07:57            3  Hot chocolate
4  2016-10-30  10:07:57            3            Jam
~~~~

### Cleaning

Reading through the data manually I saw that missing Item values are shown with NONE. These NONE rows provide no helpful data, so we can simply remove them.

~~~~python
bakery_data = bakery_data[bakery_data.Item != "NONE"]
~~~~

### Exploration

First I wanted to find the most popular items. I formed a list each unique item and counted them. For simplicity, I combined items not in the top 10 as 'Others'.

~~~~python
unique_items = bakery_data['Item'].unique()
popular_items = bakery_data.Item.value_counts()[:10]
other_items = bakery_data.Item.count() - popular_items.sum()
top_items = popular_items.append(pd.Series([other_items], index=['Others']))
~~~~

This gives us this listed result:
~~~~
Coffee           5471
Bread            3325
Tea              1435
Cake             1025
Pastry            856
Sandwich          771
Medialuna         616
Hot chocolate     590
Cookies           540
Brownie           379
Others           5499
~~~~

By a large margin, coffee is the most popular item. This sparked the idea of comparing items with coffee specifically.
I made a separate dataframe with only transactions that included coffee.

~~~~python
orders_w_coffee = bakery_data[bakery_data['Item'] == 'Coffee']['Transaction'].tolist()
bakery_copy = bakery_data
bakery_copy = bakery_copy[bakery_copy['Transaction'].isin(orders_w_coffee)]
~~~~

I make a list of the most popular items bought with coffee and how many times they were bought with coffee

~~~~python
pop_items_w_coffee = bakery_copy.Item.value_counts()[:10]
pop_items_w_coffee = pop_items_w_coffee.drop(labels=['Coffee'])
~~~~

This looks like...
~~~~
Bread            923
Cake             540
Tea              482
Pastry           474
Sandwich         421
Medialuna        345
Hot chocolate    293
Cookies          283
Toast            224
~~~~

Finally I build a dataframe with each item and their stats compared with coffee

~~~~python
vals_coffee = pop_items_w_coffee.tolist()
vals = popular_items.tolist()
vals_wo_coffee = [vals[i] - v for i,v in enumerate(vals_coffee)]

coffee_df = pd.DataFrame({'Item': pd.Series(labels), 'with_coffee': vals_coffee, 'without_coffee': vals_wo_coffee})

for dataset in [coffee_df]:
    dataset['ratio_w_coffee'] = dataset['with_coffee'] / dataset['without_coffee']
    dataset['perc_of_coffee'] = (dataset['with_coffee'] / 5471)*100
~~~~

Our resulting DataFrame
~~~~
Item  with_coffee  without_coffee  ratio_w_coffee  perc_of_coffee
0          Bread          923            2402        0.384263       16.870773
1           Cake          540             895        0.603352        9.870225
2            Tea          482             543        0.887661        8.810090
3         Pastry          474             382        1.240838        8.663864
4       Sandwich          421             350        1.202857        7.695120
5      Medialuna          345             271        1.273063        6.305977
6  Hot chocolate          293             297        0.986532        5.355511
7        Cookies          283             257        1.101167        5.172729
8          Toast          224             155        1.445161        4.094315
~~~~

### Other explorations

With the following code snippets, I found that saturday is the busiest day and the average transaction includes 2 items

~~~~python
foo = lambda a: ", ".join(a).split(', ')
bakery_data['Item'].astype('category')
aggregate = {'Transaction': 'first', 'Date': 'first', 'Time': 'first', 'Item': foo}
bakery_data = bakery_data.groupby(bakery_data['Transaction']).aggregate(aggregate)

for dataset in [bakery_data]:
    dataset['Count'] = dataset['Item'].str.len()

p = bakery_data[['Date', 'Count']].groupby('Date').sum()
p['2016-10-31': '2016-11-28'].plot()

plt.show()
~~~~

## Conclusions

Our coffee dataframe shows us some interesting findings, some expected and some not. We see that bread is the most popular coffee pairing by count with about 16% of coffee orders including bread. Since bread is also the 2nd most popular item behind coffee, this makes sense. This transaction scenario is likely someone passing through and in need of a quick snack. Another find is with Toast. Toast didn't make the top 10 items, but it is the most commonly paired item when compared with total toast orders. Since toast isn't ordered that often, but is so commonly bought with coffee, it is likely that this is a popular breakfast combo.
