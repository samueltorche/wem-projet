<template>
  <div class="film-search">

  </div>
</template>

<script>


export default {
  name: 'FilmRecommendation',
  data: function () {
    return {
      films: ['titanic'],
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

</style>
