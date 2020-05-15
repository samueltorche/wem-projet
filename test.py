import pandas as pd
# from mlxtend.frequent_patterns import apriori
# from apyori import apriori
from efficient_apriori import apriori
from mlxtend.frequent_patterns import association_rules

data_movies = pd.read_csv('movies.csv')

def label_year (row):
    return row['title'][-4:-1]

def title_without_year(row):
    return row['title'][0:-7]

data_movies['year'] = data_movies.apply(lambda row: label_year(row), axis=1)
data_movies['title'] = data_movies.apply(lambda row: title_without_year(row), axis=1)

print('this dataset contains: ', len(data_movies), 'movies')

data_ratings = pd.read_csv('ratings.csv', usecols=[0, 1])
print('this dataset contains: ', len(data_ratings), 'ratings')

limit_testing = 100000
df = data_ratings[:limit_testing].groupby(['userId','movieId']).size().reset_index(name='count')

print("Ratings effectively taken:", len(df))

basket = df.groupby(['userId', 'movieId'])['count'].sum().unstack().reset_index().fillna(0).set_index('userId')

#The encoding function
def encode_units(x):
    if x <= 0:
        return 0
    if x >= 1:
        return 1

basket_sets = basket.applymap(encode_units)

def mlxtend_mba(basket_sets):
   frequent_itemsets = apriori(basket_sets, min_support=0.1, use_colnames=True)
   rules = association_rules(frequent_itemsets, metric="lift")
   rules.sort_values('confidence', ascending = False, inplace = True)
   # rules.head(10)
   print(rules)
   
   
def apyori_mba(basket_sets, basket_len, basket_wid):
   transactions = []
   for i in range(0, basket_len):
      transactions.append([str(basket_sets.values[i,j]) for j in range(0, basket_wid)])
   rules = apriori(transactions, min_support = 0.1, min_lift=2)
   rules_list = list(rules)
   print("Number of rules found", len(rules_list))
   for item in rules:
      pair = item[0] 
      items = [x for x in pair]
      print("Rule: " + items[0] + " -> " + items[1])
      print("Support: " + str(item[1]))
      print("Confidence: " + str(item[2][0][2]))
      print("Lift: " + str(item[2][0][3]))
      print("=====================================")
      
def eff_apriori(basket_sets, basket_len, basket_wid):
   transactions = []
   for i in range(0, basket_len):
      transactions.append([str(basket_sets.values[i,j]) for j in range(0, basket_wid)])
   itemsets, rules = apriori(transactions, min_support=0.5)
   print(rules)


print("Number of transactions", len(basket_sets))
print("Number of movies", len(basket_sets.columns))   

# mlxtend_mba(basket_sets)
# apyori_mba(basket_sets, len(basket_sets), len(basket_sets.columns))
eff_apriori(basket_sets, len(basket_sets), len(basket_sets.columns))

print("------- END ---------")
