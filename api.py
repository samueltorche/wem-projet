from flask import Flask
from flask_cors import CORS
from flask import request
import requests
import pandas as pd
from flask import jsonify
import os.path
import time

# create flask variables
app = Flask(__name__)
CORS(app)

MOVIES_DATASET = 'small_dataset/movies.csv'

RATING_SUBMITTED_FILE = 'temp_ratings.csv'

RULES_DATASET = 'rules.csv'


@app.route('/get_movies', methods=['GET'])
def get_movies():
    print("GETTING LIST OF MOVIES")
    movies = get_movies_from_dataset()
    print("RECOMMENDATIONS FOUND")
    return jsonify(movies)


@app.route('/get_recommendations', methods=['GET'])
def get_recommendations():
    print("GETTING RECOMMENDATION")
    user_id = request.args.get('user_id')
    recommendations = get_recommendations_from_rating(user_id)
    print("RECOMMENDATIONS FOUND")
    return recommendations


@app.route('/add_rating', methods=['POST'])
def add_rating():
    print("ADDING RATING")
    json_result = request.json
    user_id = json_result["user_id"]
    movie_id = json_result["movie_id"]
    rating = json_result["rating"]
    # TODO add to temporary file
    result = add_rating_to_temp(user_id, movie_id, rating)
    print("RATING ADDED")
    return result
    
    
def label_year(row):
    return row['title'][-4:-1]


def title_without_year(row):
    return row['title'][0:-7]
    
    
def get_movies_from_dataset():
   data_movies = pd.read_csv(MOVIES_DATASET)
   data_movies['year'] = data_movies.apply(lambda row: label_year(row), axis=1)
   data_movies['title'] = data_movies.apply(lambda row: title_without_year(row), axis=1)
   movies = []
   for index, row in data_movies.iterrows():
      movie = {
         'movie_id': row['movieId'],
         'title': row['title'],
         'genres': row['genres'],
         'year': row['year']
      }
      movies.append(movie)
   return movies
   
   
def add_rating_to_temp(user_id, movie_id, rating):
   try:
      ts = time.time()	
      #create file
      file_obj  = open(RATING_SUBMITTED_FILE, "a+")
      file_obj.write(str(user_id) + "," + str(movie_id) + "," + str(rating) + "," + str(ts)) + "\n"
      file_obj.close()
      return 'OK'
   except Exception as exc:
      print(exc)
      return 'ERROR'

      
def get_recommendations_from_rating(user_id):
   # read rating submitted by user
   try:
      with open(RATING_SUBMITTED_FILE) as my_file:
         contents = my_file.readlines()
         my_file.close()
      movies = get_movies_from_ratings(user_id, contents)
      # check if not empty
      if len(movies) > 0:
         # get rules for movies
         rules = get_rules_for_movies(movies)
         return rules
      else:
         return 'NO RATING FOUND FOR CURRENT USER'
   except Exception as exc:
      print(exc)
      return 'ERROR'
      
 
def get_movies_from_ratings(user_id, contents):
   movies_id = []
   for line in contents:
      # split like a csv
      content = line.split(",")
      print(content)
      # check if same user_id and positive rating
      if int(content[0]) == user_id and int(content[2]) > 3:
         # add to list of movies
         movies_id.append(content[1])
   return movies_id
   
   
def get_rules_for_movies(movies):
   data_rules = pd.read_csv(RULES_DATASET)
   # TODO
   return 'OK'
   

# run the app
if __name__ == '__main__':
    app.run(debug=True, threaded=False)
