import pandas as pd
from mlxtend.frequent_patterns import apriori
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

data_ratings = data_ratings.groupby(['userId','movieId']).size().reset_index(name='count')

print(len(data_ratings))
basket = data_ratings.groupby(['userId', 'movieId'])['count'].sum().unstack().reset_index().fillna(0).set_index('userId')
print(len(basket))
basket.head(10)