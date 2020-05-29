<template>
  <div id="app">
    <img alt="Vue logo" src="./assets/logo.png">
    <FilmSearch b-vind:films=films/>
  </div>
</template>

<script>
import FilmSearch from './components/FilmSearch.vue'

export default {
  name: 'app',
  components: {
    FilmSearch
  },

  data: function () {
    return {
      films: ['titanic', 'LoTR'],
    }
  },
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
