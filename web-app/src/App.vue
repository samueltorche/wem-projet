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
      axios.get('http://localhost:5000/get_recommendations', {"movie_ids": movie_ids})
      .then((response)=>{
          console.log(response)
      })

    }
  },

  mounted: function () {
    axios
      .get('http://localhost:5000/get_movies')
      .then( (response) => {
        console.log(response.data)
        this.films = response.data
      })
  },

  data: function () {
    return {
      userid:0,
      rating:0,
      my_movies:[],
      selected_movie_id: 1,
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
      for(var idx in this.films) {
          var f = this.films[idx]
          if(f.movie_id == this.selected_movie_id) {
            return f
          }
      }
      return {}
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
