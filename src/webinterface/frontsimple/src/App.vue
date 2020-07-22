<template>
  <div id="app">
    <Chart />
    <HelloWorld />
    <StepperVertical />
  </div>
</template>

<script>
import Chart from './components/Chart.vue'
import HelloWorld from './components/HelloWorld.vue'
import StepperVertical from './components/Stepper.vue'

export default {
  name: 'App',
  components: {
    Chart,
    HelloWorld,
    StepperVertical
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
