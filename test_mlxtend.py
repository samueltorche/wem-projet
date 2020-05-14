import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
from mlxtend.preprocessing import TransactionEncoder

data_movies = pd.read_csv('movies.csv')


def label_year(row):
    return row['title'][-4:-1]


def title_without_year(row):
    return row['title'][0:-7]


data_movies['year'] = data_movies.apply(lambda row: label_year(row), axis=1)
data_movies['title'] = data_movies.apply(lambda row: title_without_year(row), axis=1)

print('this dataset contains: ', len(data_movies), 'movies')

data_ratings = pd.read_csv('ratings.csv', usecols=[0, 1])
print('this dataset contains: ', len(data_ratings), 'ratings')

limit_testing = 100000
df = data_ratings.groupby(['userId', 'movieId']).size().reset_index(name='count')

print("Ratings effectively taken:", len(df))

basket = df.groupby(['userId', 'movieId'])['count'].sum().unstack().reset_index().fillna(0).set_index('userId')


# The encoding function
def encode_units(x):
    if x <= 0:
        return 0
    if x >= 1:
        return 1


basket_sets = basket.applymap(encode_units)


def mlxtend_mba(basket_sets):
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
    rules = association_rules(frequent_itemsets, metric="lift")
    rules.sort_values('confidence', ascending=False, inplace=True)
    # rules.head(10)
    print(rules)


print("Number of transactions", len(basket_sets))
print("Number of movies", len(basket_sets.columns))
mlxtend_mba(basket_sets)

print("------- END ---------")
