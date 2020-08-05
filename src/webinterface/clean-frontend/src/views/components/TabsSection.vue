<template>
  <div class="wrapper">
    <div id="nav-tabs">
      <h3>HowTo Section</h3>
      <div class="md-layout">

        <div class="md-layout-item md-size-100 md-small-size-100">
          <h3><small>Getting started</small></h3>
          <nav-tabs-card no-label tabs-plain>
            <template slot="content">
              <md-tabs class="md-danger" md-alignment="left">
                <md-tab id="tab-home" md-label="FAQ" md-icon="info">
                  <h3>Frequently Asked Questions and Answers</h3>
                  <p>
                    Our goal was to make this web interface as user-friendly and intuitive 
                    as possible. If you are still in confusion, you can almost certainly 
                    find an answer in the following tabs. 
                  </p>
                </md-tab>

                <md-tab id="tab-pages" md-label="How to use">
                  
                  <p>
                    The function of this machine learning projects is to predict the 
                    increased usage of internet traffic depending on the corona cases.                    
                  </p>
                  <p>
                  1. Select a time frame in which the forecast should be made.
                  </p>
                  <p>
                  2. Select a topic on which the prediction should be made.
                  </p>
                  <p>
                  3. Click on the Button "Run inference" to run the prediction.
                  </p>

                </md-tab>

                <md-tab id="tab-posts" md-label="History">
                  <p>
                    In the past, it has always been relatively easy to predict how 
                    much traffic the Internet will have. Internet traffic is highly 
                    seasonal, depending on time of day, day of the week and month. 
                    It depends very much on the company that you get data over a long 
                    period of time. If you look at data over several years, you can 
                    see that there is a steady upward trend in addition to the seasonality.

                    However, Corona and its political measures have led to these 
                    patterns being broken and to an abrupt rise. This has pushed 
                    many companies to their limits, which has reduced the quality 
                    of some streaming services. 
                    
                    The model we have created is designed to help predict future 
                    internet traffic during the Corona pandemic and possible future 
                    pandemics.


                  </p>
                </md-tab>

                <md-tab id="tab-e-mail" md-label="Further Questions">
                  <p>
                    If you have any further questions, please feel free 
                    to contact us at the following e-mail address: n.landerer@tum.de
                  </p>
                </md-tab>
                
              </md-tabs>
            </template>
          </nav-tabs-card>
        </div>


        <div class="md-layout-item md-size-100 md-small-size-100">
          <h3><small>Data Collection</small></h3>
          <nav-tabs-card no-label tabs-plain>
            <template slot="content">
              <md-tabs class="md-primary" md-alignment="left">
                <md-tab id="tab-home" md-label="FAQ" md-icon="info">
                 <h3>wie wir an unsere Daten gekommen sind</h3>
                  <p>
                    I think that’s a responsibility that I have, to push
                    possibilities, to show people, this is the level that things
                    could be at. So when you get something that has the name
                    Kanye West on it, it’s supposed to be pushing the furthest
                    possibilities. I will be the leader of a company that ends
                    up being worth billions of dollars, because I got the
                    answers. I understand culture. I am the nucleus.
                  </p>
                </md-tab>

                <md-tab id="tab-pages" md-label="Data sources">
                  <p>
                    I will be the leader of a company that ends up being worth
                    billions of dollars, because I got the answers. I understand
                    culture. I am the nucleus. I think that’s a responsibility
                    that I have, to push possibilities, to show people, this is
                    the level that things could be at. I think that’s a
                    responsibility that I have, to push possibilities, to show
                    people, this is the level that things could be at.
                  </p>
                </md-tab>

                <md-tab id="tab-posts" md-label="preprocessing">
                  <p>
                    I think that’s a responsibility that I have, to push
                    possibilities, to show people, this is the level that things
                    could be at. I will be the leader of a company that ends up
                    being worth billions of dollars, because I got the answers.
                    I understand culture. I am the nucleus. I think that’s a
                    responsibility that I have, to push possibilities, to show
                    people, this is the level that things could be at.
                  </p>
                </md-tab>
              </md-tabs>
            </template>
          </nav-tabs-card>
        </div>


      </div>
    </div>
  </div>
</template>

<script>
import { NavTabsCard } from "@/components";

export default {
  components: {
    NavTabsCard
  }
};
</script>

<style lang="css"></style>
