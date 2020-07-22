<template>
    <div class="md-layout md-gutter">
      <div class="md-layout-item">
        <form>
        <md-field>
          <label for="movie">Movie</label>
          <md-select v-model="movie" name="movie" id="movie" >
            <md-option value="1">Fight Club</md-option>
            <md-option value="2">Godfather</md-option>
            <md-option value="3">Godfather II</md-option>
            <md-option value="4">Godfather III</md-option>
            <md-option value="5">Godfellas</md-option>
            <md-option value="6">Pulp Fiction</md-option>
            <md-option value="7">Scarface</md-option>
          </md-select>
        </md-field>
        </form>
        <md-button @click='getDatasetValue()'>submit</md-button>
        
        <h1 v-if="movie">Predicted Class is: {{ movie }}</h1>   
      </div>
  </div>
</template>

<script>

export default {
  name: 'Dropdown',
  data: () => ({
        movie: '1',
        country: null,
        font: null,
      }),
  props: {
    movie: Int8Array
  },    
  methods: { 
    getDatasetValue (){
      this.$emit('getDatasetValue',this.movie)
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
