<template>
  <div id="app">
    <div class="topbar">
      <Topbar />
    </div>
    <div class="content">
      <Chart />
      <HelloWorld />
      <StepperVertical />
    </div>
  </div>
</template>

<script>
import Topbar from './components/Topbar.vue'
import Chart from './components/Chart.vue'
import HelloWorld from './components/HelloWorld.vue'
import StepperVertical from './components/Stepper.vue'

export default {
  name: 'App',
  components: {
    Topbar,
    Chart,
    HelloWorld,
    StepperVertical
  }
}
</script>

<style>
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
