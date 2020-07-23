<template>
  <div class="small">
    <line-chart :chart-data="datacollection"></line-chart>
    <button @click="fillData()">Randomize</button>
    <u1> Predicted Class is: {{ datacollection }}</u1>  
  </div>
</template>

<script>
  import LineChart from './LineChart.js'

  export default {
    components: {
      LineChart
    },
    props: {
    data: Int8Array
    }, 
    data () {
      return {
        datacollection: null, 
        
      }
    },
    mounted () {
      this.fillData()
    },
    methods: {
      fillData () {
        this.datacollection = {
          labels: [0, 1, 2, 3, 4 ,5 ,6 ,7,8, 9],
          datasets: [
            {
              label: 'Data One - test',
              backgroundColor: '#004c99',
              data: this.data
            }
          ]
        }
      },
      getRandomInt () {
        return Math.floor(Math.random() * (50 - 5 + 1)) + 5
      }
    }
  }
</script>

<style>
  .small {
    max-width: 600px;
    margin:  20px;
  }
</style>

import Chart from './components/Chart.vue'
    Chart,