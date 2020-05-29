<template>
  <div class="film-search">
    <h1>Film Search</h1>
    <form>
      <p>{{films}}</p>
      <p>{{filtered_films}}</p>
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
  mounted: function () {
    /*axios
      .get('https://api.coindesk.com/v1/bpi/currentprice.json')
      .then(response => (this.films = response))*/
  },
  computed: {
    filtered_films: function () {
      return this.films.filter( (film) => {
        return film.startsWith(this.search_value)
      })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
