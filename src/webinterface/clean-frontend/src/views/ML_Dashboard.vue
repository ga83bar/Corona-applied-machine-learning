<template>
  <div class="wrapper">
  <notifications></notifications>
    <parallax
    class="section page-header header-filter"
    :style="headerStyle"
  ></parallax>
    <div class="main main-raised">
      <div class="section profile-content">
        <div class="container">

        
        
        <div class="md-layout">
          <line-chart :chart-data="datacollection"/>    
          <u1> Predicted Class is: {{ datacollection }}</u1> 
          
          <div class="md-layout-item md-size-66 mx-auto">
          


          <div class="controls">
            <div class="md-layout md-gutter">
              <div class="md-layout-item">
                <form>
                <md-field>
                  <label for="model">Model selection</label>
                  <md-select v-model="model" name="model" id="model">
                    <md-option value="1">Internet Exchange Points</md-option>
                    <md-option value="2">Playstation</md-option>
                    <md-option value="3">Adult Websites</md-option>
                    <md-option value="4">Google statistics</md-option>
                    <md-option value="5">Twitch</md-option>
                    <md-option value="6">Foo bar</md-option>
                    <md-option value="7">Hello World</md-option>
                  </md-select>
                </md-field>
              </form>
              </div>
               <div class="md-layout-item buttonbed">
               <md-button class="md-success md-round run" @click='select_set()'>Run Inference</md-button>
               
               </div>
               <u1 v-if="model">Predicted Class is: {{ model }}</u1>
            </div>
            </div>
          <div class="hor-space">
          </div>
          
            <div class="md-layout md-gutter">

                <div class="">
                <md-button
                    class="md-success"
                    @click="notifyVue('top', 'center', 'success', 'Connection established.')"
                    >successful notification</md-button
                  >
              </div>
              <div class="">
               <md-button
                    class="md-danger"
                    @click="notifyVue('top', 'center', 'danger', 'Connection failed.')"
                    >failure notification</md-button
                  >
              </div>
          
            </div>
            

       
    
          </div>
        </div>
       
          <div class="profile-tabs">
            <tabs
              :tab-name="['Studio', 'Work', 'Favorite']"
              :tab-icon="['camera', 'palette', 'favorite']"
              plain
              nav-pills-icons
              color-button="success"
            >
          
         
            </tabs>
          </div>





        </div>
      </div>
    </div>
  </div>
</template>

<script>
//import { Tabs } from "@/components";
import Tabs from "./components/TabsSection";
import axios from 'axios'
import LineChart from './components/LineChart.js'

export default {
  components: {
    Tabs,
    LineChart
  },
  bodyClass: "profile-page",
  data() {
    return {
      model: '1',
      datacollection : null
    }
  },

  methods: {

    notifyVue(verticalAlign, horizontalAlign, type_notification, notify_message) {
      var color = Math.floor(Math.random() * 4 + 1);
      this.$notify({
        message: notify_message,
        icon: "add_alert",
        horizontalAlign: horizontalAlign,
        verticalAlign: verticalAlign,
        type: type_notification
      });
    },
      select_set(){
      axios.post('http://127.0.0.1:5000/predict', {
        dataset_req: this.model
      })
      .then(response => {
        this.acceptedRequest = response.data.class
        this.datacollection = {
          labels: [0, 1, 2, 3, 4 ,5 ,6 ,7,8, 9],
          datasets: [
            {
              label: 'Data One - test',
              backgroundColor: '#004c99',
              data: response.data.chart_data
            }
          ]
        }
                
      })
      .catch(e => {
        notifyVue('top', 'center', 'danger', 'Connection failed.')
      })

   }

  },
  props: {
    header: {
      type: String,
      default: require("@/assets/img/background.jpg")
    }
  },
  computed: {
    headerStyle() {
      return {
        backgroundImage: `url(${this.header})`
      };
    }
  }
};
</script>

<style lang="scss" scoped>
.section {
  padding: 0;
}

.profile-tabs::v-deep {
  .md-card-tabs .md-list {
    justify-content: center;
  }

  [class*="tab-pane-"] {
    margin-top: 3.213rem;
    padding-bottom: 50px;

    img {
      margin-bottom: 2.142rem;
    }
  }
}

.main-raised
{
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto
}


.controls{
  margin-top:40px;
}

.buttonbed{
position:relative;
}

.run{
  position: absolute;
  left: 25%;
}

/* chart */

.chartjs
{
  max-width: 950px;
  margin-left:  auto;
  margin-right:  auto;
  margin-top: 100px;
}

/* page */
.profile-page{
    .page-header{
        height: 180px;
        background-position: center center;

        &::before {
          background: rgba(0,0,0, .2);
        }
    }

}

.hor-space{
  height:75px;
}

</style>
