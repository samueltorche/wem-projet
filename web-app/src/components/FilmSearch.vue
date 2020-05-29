<template>
  <div class="film-search">
    <h1>Film Search</h1>
    <form>
      
      <div class="films-sorted">
        <div
          class="ff"
          v-for="ff in filtered_films" :key=ff.title
          v-on:click="selectmovie(ff.movie_id)"
        >
          <div class="ff-title">{{ff.title}}</div>
          <div class="ff-year">{{ff.year}}</div>
          <div class="ff-genres">{{ff.genres}}</div>
        </div>
      </div>


      <p>{{search_value}}</p>
      <input v-model="search_value" type="text" placeholder="Titanic">
      <input type="button" value="Ajouter">
    </form>
  </div>
</template>

<script>


export default {
  name: 'FilmSearch',
  props: ['films'],
  data: function () {
    return {
      search_value: ""
    }
  },


  methods: {
    selectmovie: function(movie_id) {
      this.$emit('update', movie_id)
    }
  },

  computed: {
    filtered_films: function () {
      //if (this.search_value.length < 3) { return []}

      return this.films.filter( (film) => {
        return film.title.startsWith(this.search_value)
      })
    }
  }
}
</script>

<style>
.films-sorted {
  display: flex;
}

.ff {
  background: #e3e3e3;
  color: #122323;
  height: 100px;
  width: 200px;
  text-align: center;
  margin: 5px 15px;
  display: flex;
  flex-direction: column;
}

.ff-title {
  font-weight: bold;
  font-size: 20px;
}
</style>
