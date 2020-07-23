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
       <img src="./../assets/img/js.png" class="chartjs">
          
          <div class="md-layout-item md-size-66 mx-auto">
          


          <div class="controls">
            <div class="md-layout md-gutter">
              <div class="md-layout-item">
                <md-field>
                  <label for="movie">Model selection</label>
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
               <div class="md-layout-item buttonbed">
               <md-button class="md-success md-round run">Run Inference</md-button>
               </div>
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


export default {
  components: {
    Tabs
  },
  bodyClass: "profile-page",
  data() {
    return {
  
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
