<template>
  <div id="app">
    <div class="topbar">
      <Topbar />
    </div>
      <div class="content">
        <div class="small">
          <line-chart :chart-data="datacollection"></line-chart>    
          <u1> Predicted Class is: {{ datacollection }}</u1>  
      </div>
      <Dropdown :movie="movievalue" @getDatasetValue="select_set($event)"/>
      <StepperVertical />
      <h1 v-if="movievalue">Predicted Class is: {{ movievalue }}</h1>
      <h1 v-if="acceptedRequest">Predicted Class is: {{ acceptedRequest}}</h1>
      <h1 v-if="charst_data">Predicted Class is: {{ charts_data}}</h1>
      <ul v-if="errors ">        
        {{errors.message}}        
      </ul>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import Topbar from './components/Topbar.vue'
import Dropdown from './components/Dropdown.vue'
import StepperVertical from './components/Stepper.vue'
import LineChart from './components/LineChart.js'

export default {
  name: 'App',
  components: {
    Topbar,
    Dropdown,
    StepperVertical,
    LineChart
  },
   data() {
   return {               
      errors: [],
      charts_data: null,
      movievalue: null
    }
  },
  mounted () {
      this.select_set()
    },
  methods: {
   select_set(temp){
     this.movievalue=temp,
      axios.post('http://127.0.0.1:5000/predict', {
        dataset_req: temp
      })
      .then(response => {
        this.acceptedRequest = response.data.class
        this.charts_data = response.data.chart_data
        this.datacollection = {
          labels: [0, 1, 2, 3, 4 ,5 ,6 ,7,8, 9],
          datasets: [
            {
              label: 'Data One - test',
              backgroundColor: '#004c99',
              data: this.charts_data
            }
          ]
        }
        return this.datacollection
      })
      .catch(e => {
        this.errors.push(e)
      })
   }
  }
}
</script>




<style>
.small {
  max-width: 600px;
  margin:  20px;
}
.topbar{
  text-align: right;
}
.content{
  margin-left: 5%;
  margin-right: 5%;
  align-self: center;
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 0px;
  background-color: white;
}
</style>
