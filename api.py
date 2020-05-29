from flask import Flask
from flask_cors import CORS
from flask import request
import requests
import pandas as pd
from flask import jsonify

# create flask variables
app = Flask(__name__)
CORS(app)


@app.route('/get_movies', methods=['GET'])
def get_movies():
    print("GETTING LIST OF MOVIES")
    movies = get_movies()
    print("RECOMMENDATIONS FOUND")
    return jsonify(movies)


@app.route('/get_recommendations', methods=['POST'])
def get_recommendations():
    json_result = request.json
    query_value = json_result["query"]
    print("GETTING RECOMMENDATION")
    # TODO
    print("RECOMMENDATIONS FOUND")
    return 0


@app.route('/add_ratings', methods=['POST'])
def add_ratings():
    json_result = request.json
    query_value = json_result["ratings"]
    print("ADDING RECOMMENDATIONS")
    # TODO
    print("RECOMMENDATION ADDED")
    return 'OK'
    
    
def label_year(row):
    return row['title'][-4:-1]


def title_without_year(row):
    return row['title'][0:-7]
    
    
def get_movies():
   data_movies = pd.read_csv('small_dataset/movies.csv')
   data_movies['year'] = data_movies.apply(lambda row: label_year(row), axis=1)
   data_movies['title'] = data_movies.apply(lambda row: title_without_year(row), axis=1)
   print(data_movies)
   movies = []
   for index, row in data_movies.iterrows():
      movie = {
         'movie_id': row['movieId'],
         'title': row['title'],
         'genres': row['genres'],
         'year': row['year']
      }
      movies.append(movie)
   result = {
      'list_of_movies': movies
   }
   return movies


# run the app
if __name__ == '__main__':
    app.run(debug=True, threaded=False)
