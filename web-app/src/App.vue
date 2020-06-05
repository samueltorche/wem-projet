<template>
  <div id="app">

    <h1>User ID</h1>
    <input v-model="userid" type="text">

    <FilmSearch v-bind:films="films" @update="setSelectedMovie"/>

    <div id="selected_movie">
      <div class="sm-title">{{selected_movie.title}}</div>
      <div class="sm-year">{{selected_movie.year}}</div>
      <div class="sm-genres">{{selected_movie.genres}}</div>
      <div class="sm-ratings">
        <!--
        <div class="sm-circle"></div>
        <div class="sm-circle"></div>
        <div class="sm-circle"></div>
        <div class="sm-circle"></div>
        <div class="sm-circle"></div>-->
        <input v-model="rating" type="text">
        <input type="button" v-on:click="submit_rating()" value="Add rating" />
      </div>
      <input type="button" v-on:click="add_wish()" value="Add to My Movies" />
    </div>


    <br/>
    <br/>
    <br/>
    <br/>
    <br/>

    
    <div class="my-movies">
      <div v-for="m in my_movies" :key="m.movie_id">
        {{m.title}}
      </div>
    </div>
    <input type="button" v-on:click="get_recommendations()" value="Get Recommendations" />
    <div>
      {{recommended_movies}}
    </div>
  </div>
</template>

<script>
import FilmSearch from './components/FilmSearch.vue'
const axios = require('axios')

export default {
  name: 'app',
  components: {
    FilmSearch
  },

  methods: {
    setSelectedMovie: function(movie_id) {
      console.log("Selected movie", movie_id)
      this.selected_movie_id = movie_id
    },

    add_wish: function(){
      this.my_movies.push(this.selected_movie)
    },

    submit_rating: function() {
      const uid = parseInt(this.userid);
      const r = parseInt(this.rating);
      this.selected_movie_id;

      axios.post('http://localhost:5000/add_rating', {"user_id": uid, "movie_id":this.selected_movie_id, "rating":r}
        )
      .then(function(result){
        console.log(result)
      })
    },

    get_recommendations: function() {

      var movie_ids = []
      for(var idx in this.my_movies) {
        var m = this.my_movies[idx]
        movie_ids.push(m.movie_id)
      }

      
      var request_param ="movie_id="
      var isfirst = true
      for(var mid in movie_ids ){
        if (isfirst) {
          request_param +=  movie_ids[mid]
          isfirst = false
          continue
        }
        request_param += "&movie_id=" + movie_ids[mid]
      }

      console.log(request_param)

      axios.get('http://localhost:5000/get_recommendations?'+request_param, {})
      .then((response)=>{
          console.log("RESPONSE")
          var recommendations = response.data
          var movies_id_rec = []
          for(var i=0; i<recommendations.length; i++) {
            var sub_recs = recommendations[i]
            movies_id_rec.push(sub_recs)
          }

          this.recommended_movies_ids = movies_id_rec

      })

    }
  },

  mounted: function () {
    axios
      .get('http://localhost:5000/get_movies')
      .then( (response) => {

        var indexes_movies = {}

        console.log(response.data)
        this.films = response.data

        for (var i = 0; i < response.data.length; i++) {
          var m = response.data[i]
          indexes_movies[m.movie_id] = m
        }

        this.indexes_movies = indexes_movies

      })
  },

  data: function () {
    return {
      userid:0,
      rating:0,
      my_movies:[],
      selected_movie_id: 1,
      recommended_movies_ids: [],
      films: [
        {
          "genres": "Adventure|Animation|Children|Comedy|Fantasy", 
          "movie_id": 1, 
          "title": "Toy Story", 
          "year": "995"
        }, 
        {
          "genres": "Adventure|Children|Fantasy", 
          "movie_id": 2, 
          "title": "Jumanji", 
          "year": "995"
        }, 
      ]
    }
  },

  computed: {
    selected_movie: function () {
      //if (this.search_value.length < 3) { return []}
      return this.indexes_movies[this.selected_movie_id]
    },

    recommended_movies: function() {
      var res = []
      if (this.recommended_movies_ids.length==0) { return []}
      for(var idx in this.recommended_movies_ids) {
          var fid = this.recommended_movies_ids[idx]
          res.push(this.indexes_movies[fid].title)
      }
      return res
    }
  }
}
</script>

<style>
*{
  margin: 0;
  paddin: 0;
}

#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;

  background: #232323;
  padding: 60px;
  color: white;

  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}


#selected_movie {
  display:flex;
  flex-direction: column;
  color: #232323;
  background: #fcfcfc;
  height: 300px;
  width: 300px;
  justify-content: center;
  align-items: center;
}

.sm-ratings {
  margin-top: 100px;
  display:flex;
  flex-direction: row;
  justify-content: center;
}

.sm-circle{
  background: #232323;
  height: 20px;
  width: 20px;
  border-radius: 50%;
}

.sm-title {
  font-size: 25px;
  font-weight: bold;
}

</style>
