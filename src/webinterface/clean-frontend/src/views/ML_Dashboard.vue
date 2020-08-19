<template>
  <div class="wrapper"><div class="top-pinned">
  <notifications></notifications>
  </div>
    <parallax
    class="section page-header header-filter"
    :style="headerStyle"
  ></parallax>
    <div class="main main-raised">
      <div class="section profile-content">
        <div class="container">

        
        
        <div class="md-layout mx-auto">
          <div class="fsize-chart">
          <line-chart :chartData="chartdata" :chartLabels="chartlabels"/>  
          </div> 
          <div v-if="chartdata"> Predicted Class is: {{ chartdata }}</div> 
          <div class="md-layout-item ">

          <div class="controls">
            <div class="md-layout md-gutter">
              <div class="md-layout-item">
                <form>
                <md-field>
                  <label for="model">Model selection</label>
                  <md-select v-model="model" name="model" id="model" md-direction="bottom-end">
                    <md-option @click='select_set()' value="1"> Internet Exchange Points</md-option>
                    <md-option value="2"> Playstation</md-option>
                    <md-option value="3"> Adult Websites</md-option>
                    <md-option value="4"> Google statistics</md-option>
                    <md-option value="5"> Twitch</md-option>
                    <md-option value="6"> Foo bar</md-option>
                    <md-option value="7"> Hello World</md-option>
                  </md-select>
                </md-field>
              </form>
              </div>
               <div class="md-layout-item buttonbed">
                  <md-button class="md-success md-round run" @click='select_set()'>Run Inference</md-button>
               </div>
               <u1 v-if="model">Predicted Class is: {{ model }}</u1>
            </div>

            <div class="md-layout md-gutter">
              <div class="md-layout-item">
                <md-menu md-size="medium" md-align-trigger>
                  <md-button md-menu-trigger>{{selectedDataset}}</md-button>
                  <md-menu-content>
                    <md-menu-item @click="model='1', select_set(), selectedDataset='Internet Exchange Points'">Internet Exchange Points</md-menu-item>
                    <md-menu-item @click="model='2', select_set(), selectedDataset='Playstation'">Playstation</md-menu-item>
                    <md-menu-item @click="model='3', select_set(), selectedDataset='Item 3'">My Item 3</md-menu-item>
                  </md-menu-content>
                </md-menu>
              </div>
              <div class="md-layout-item buttonbed" :class="`md-alignment-top-left`">
                  <md-button class="md-success md-round run" @click='select_set()'>Run Inference</md-button>
               </div>
               <u1 v-if="model">Predicted Class is: {{ model }}</u1>
            </div>
            
            <div class="block">
              <div class="md-layout md-gutter" :class="`md-alignment-top-left`">
                <div class="md-layout-item md-size-35">
                <h3>Start Date</h3>
                <md-datepicker v-model="start_date" :md-disabled-dates="disabledDates"/>          
                </div>
                <div class="md-layout-item md-size-35">        
                <h3>End Date</h3>
                <md-datepicker v-model="end_date" :md-model-type="string"  /> 
                </div>
              </div>
            </div>
            

          </div>
          <div class="hor-space mx-auto"></div>
          
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
       
        <div class="profile-tabs mx-auto">
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
import LineChart from './components/LineChart.vue'
import format from 'date-fns/format'

export default {
  components: {
    Tabs,
    LineChart
  },
  bodyClass: "profile-page",
  data() {
    let dateFormat = this.$material.locale.dateFormat || 'yyyy-MM-dd'
    let now = new Date()

    return {
      start_date: format(now, dateFormat),
      end_date: format(now, dateFormat),
      selectedDataset: 'Select dataset',
      disabledDates: function(date) {
        // compare if today is greater then the datepickers date
      },
      model: '1',
      chartdata : null,
      chartlabels: null,
      datecheck_bool: null,
      chart: { 
        responsive: true,
        maintainAspectRatio: true,
        aspectRatio: 2
      }
      

    }
  },
  computed:{
    // eslint-disable-next-line

      dateFormat () {
        return this.$material.locale.dateFormat || 'yyyy-MM-dd'
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
        dataset_req: this.model,
        start_date_req: this.start_date,
        end_date_req: this.end_date
      })
      .then(response => {
        this.acceptedRequest = response.data.class,        
        this.chartlabels = response.data.labels,
        this.chartdata = 
          [
            {
              label: 'Data One - test',
              data: response.data.chart_data_1,
					    borderColor: 'rgb(238, 76, 96)',
              fill: false
            },
            {
              label: 'Data two - test',
              data: response.data.chart_data_2,
              borderColor: 'rgb(76, 175, 80)',
              fill: false
            }
          ]
        this.datecheck_bool = response.data.datecheck,
        this.checkdate(this.datecheck_bool);
          
                
      })
      .catch(e => {
        this.notifyVue('top', 'center', 'danger', 'Connection failed.')
      })

   },
      toString () {
        this.toDate()
        this.dynamicByModel = this.dynamicByModel && format(this.dynamicByModel, this.dateFormat)
      },
      disableTo(val) {
      if (typeof this.disabled.to === "undefined") {
        this.disabledDates = {
          to: null,
          daysOfMonth: this.disabledDates.daysOfMonth,
          from: this.disabled.from
        };
      }
      this.disabledDates.to = val;
    },
    checkdate(bool){
      if(bool== 1){        
        this.notifyVue('top', 'center', 'danger', 'End-date > Start-date.');
      }
    },
    disableFrom(val) {
      if (typeof this.disabledDates.from === "undefined") {
        this.disabled = {
          to: this.disabledDates.to,
          daysOfMonth: this.disabled.daysOfMonth,
          from: null
        };
      }
      this.disabledDates.from = val;
    },

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
    justify-content: left;
  }

  [class*="tab-pane-"] {
    margin-top: 3.213rem;
    padding-bottom: 50px;

    img {
      margin-bottom: 2.142rem;
    }
  }
}

.block{
  max-height: relative;
}

.main-raised
{
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
}


.controls{
  margin-top:40px;
  margin-right: 10px;

}

.buttonbed{
position:relative;
}

.run{
  position: absolute;
  left: 25%;
}

/* chart */

.top-pinned
{
  position:fixed;
  width:100%;
  top: 0;
  z-index: 9000;
  background: transparent
}

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

.fsize-chart 
{
  width:100%;
}

.hor-space{
  height:75px;
}

</style>
