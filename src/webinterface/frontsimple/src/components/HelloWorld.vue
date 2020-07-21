<template>
    <div class="md-layout md-gutter">
      <div class="md-layout-item">
        <md-field>
          <label for="movie">Movie</label>
          <md-select v-model="movie" name="movie" id="movie">
            <md-option value="fight-club">Fight Club</md-option>
            <md-option value="godfather">Godfather</md-option>
            <md-option value="godfather-ii">Godfather II</md-option>
            <md-option value="godfather-iii">Godfather III</md-option>
            <md-option value="godfellas">Godfellas</md-option>
            <md-option value="pulp-fiction">Pulp Fiction</md-option>
            <md-option value="scarface">Scarface</md-option>
          </md-select>
        </md-field>
      </div>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  data: () => ({
        movie: 'godfather',
        country: null,
        font: null
      })
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
