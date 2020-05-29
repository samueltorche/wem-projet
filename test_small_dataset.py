import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import fpgrowth
from mlxtend.frequent_patterns import association_rules
from mlxtend.preprocessing import TransactionEncoder

data_movies = pd.read_csv('small_dataset/movies.csv')


def label_year(row):
    return row['title'][-4:-1]


def title_without_year(row):
    return row['title'][0:-7]


data_movies['year'] = data_movies.apply(lambda row: label_year(row), axis=1)
data_movies['title'] = data_movies.apply(lambda row: title_without_year(row), axis=1)

print('this dataset contains: ', len(data_movies), 'movies')

data_ratings = pd.read_csv('small_dataset/ratings.csv', usecols=[0, 1, 2])
print('this dataset contains: ', len(data_ratings), 'ratings')
data_ratings = data_ratings[data_ratings.rating > 2]
print('this dataset contains: ', len(data_ratings), 'positive ratings')

df = data_ratings.groupby(['userId', 'movieId']).size().reset_index(name='count')

print("Ratings effectively taken:", len(df))

print("Creation of basket dataframe...")
basket = df.groupby(['userId', 'movieId'])['count'].sum().unstack().reset_index().fillna(0).set_index('userId')
print("Basket dataframe created...")


# The encoding function
def encode_units(x):
    if x <= 0:
        return 0
    if x >= 1:
        return 1


print("Encoding basket sets...")
# basket_sets = basket.applymap(encode_units)
basket_sets = basket
print("Basket sets encoded")


def mlxtend_mba(basket_sets):
   '''
   transactions = []
   for i in range(0, len(basket_sets)):
      t = []
      for j in range(0, len(basket_sets.columns)):
         if(basket_sets.values[i,j] == 1):
            t.append(list(basket_sets)[j])
      transactions.append(t)

   te = TransactionEncoder()
   oht_ary = te.fit(transactions).transform(transactions, sparse=True)
   sparse_df = pd.DataFrame.sparse.from_spmatrix(oht_ary, columns=te.columns_)
   sparse_df.columns = [str(i) for i in sparse_df.columns]

   frequent_itemsets = apriori(sparse_df, min_support=0.1, use_colnames=True)
   '''
   print("Applying fpgrowth/apriori on baskets...")
   frequent_itemsets = fpgrowth(basket_sets, min_support=0.2, use_colnames=True)
   # frequent_itemsets = apriori(basket_sets, min_support=0.3, use_colnames=True, low_memory=True)
   print("Applying association rules...")
   rules = association_rules(frequent_itemsets, metric="lift")
   print("Sorting association rules...")
   rules.sort_values('confidence', ascending=False, inplace=True)
   # rules.head(10)
   print("Number of rules found:", len(rules))
   print(rules)
   # save rules
   filename = 'rules.csv'
   rules.to_csv(filename, index=False)
   print("Rules saved to file:", filename)


print("Number of transactions", len(basket_sets))
print("Number of movies", len(basket_sets.columns))
mlxtend_mba(basket_sets)

print("------- END ---------")
