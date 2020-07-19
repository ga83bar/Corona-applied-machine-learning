<template>
  <div >      
    

    <form>
    <md-field>
      <label>SepalLength</label>
      <md-input v-model="sepalLength" placeholder="A nice placeholder"></md-input>
    </md-field>

    <md-field>
      <label>sepalWidth</label>
      <md-input v-model="sepalWidth" placeholder="A nice placeholder"></md-input>
    </md-field>

    <md-field>
      <label>petalLength</label>
      <md-input v-model="petalLength" placeholder="A nice placeholder"></md-input>
    </md-field>

    <md-field>
      <label>petalWidth</label>
      <md-input v-model="petalWidth" placeholder="A nice placeholder"></md-input>
    </md-field>

    <md-button @click="submit">submit</md-button>
    <md-button @click="clear">clear</md-button>
    </form>
    <h1 v-if="predictedClass">Predicted Class is: {{ predictedClass }}</h1>   
    
  </div>
</template>


<script>
  import axios from 'axios'
  export default {
    name: 'HelloWorld',
    data: () => ({
      sepalLength: '',
      sepalWidth: '',
      petalLength: '',
      petalWidth: '',
      predictedClass : '',
      showNavigation: false,
      showSidepanel: false
    }),
    methods: {
    submit () {
      axios.post('http://127.0.0.1:5000/predict', {
        sepal_length: this.sepalLength,
        sepal_width: this.sepalWidth,
        petal_length: this.petalLength,
        petal_width: this.petalWidth
      })
      .then((response) => {
        this.predictedClass = response.data.class
      })
    },
    clear () {
      this.sepalLength = ''
      this.sepalWidth = ''
      this.petalLength = ''
      this.petalWidth = ''
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
.page-container {
  min-height: 300px;
  overflow: hidden;
  position: relative;
  border: 1px solid rgba(#000, .12);
}

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








