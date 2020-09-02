<template>
  <div class="wrapper">
    <div id="nav-tabs">
      <h3>Background Section</h3>
      <div class="md-layout">

        <div class="md-layout-item md-size-100 md-small-size-100">
          <h3><small>Getting started</small></h3>
          <nav-tabs-card no-label tabs-plain>
            <template slot="content">
              <md-tabs class="md-danger" md-alignment="left">
                <md-tab id="tab-how-to" md-label="How to use what_if.ai">
                  
                  <p>
                    In order to model global economic and online traffic trends, what if.ai provides many different data sets to choose from. These range from medical
                    and tech stock projections for the economic data to more specific ones such
                    as internet exchange point bitrates and twitch statistics for the internet
                    traffic analysis.                  
                  </p>
                  <p>
                  Simply select your desired data set and let the AI model do its magic.
                  The resulting model prediction is displayed in green alongside the original
                  true data in red. Additionally, common error metrics such as the MSE
                  and R2 are given and confidence intervals are displayed in gray in order
                  to give a perception of how good the prediction is.
                  </p>

                </md-tab>

                <md-tab id="tab-about-the-model" md-label="About the AI Model">
                  <p>
                    The main goal of the what if.ai project is to forecast time series for the
                    respective data sets. To this, we prefer to use <b>Prophet</b>, a forecasting
                    framework provided by Facebook.<br><br>

                    Prophet is based on an additive model composition where non-linear trends
                    are being fit with either yearly, weekly or daily seasonality. As such, it
                    perfectly suits our time series modeling task. Furthermore, it promises to
                    be especially robust to missing data or shifts in the trend itself and thus
                    handles outliers very well.<br>
                    <b>How it works</b><br>
                    Prophet is an additive regression model with four main components:<br><br>
                    (a) A piecewise linear or logistic growth curve trend
                    (Detects changes in trends automatically by selecting changepoints
                    from the data)<br>
                    (b) A yearly seasonal component modeled using Fourier series<br>
                    (c) A weekly seasonal component using dummy variables<br>
                    (d) A user-provided list of important events (i.e. holidays, etc.)<br><br>

                    The main idea is to very flexibly fit the trend component which leads to
                    a better identification of the model seasonality and thus a more accurate
                    forecast. This is done by choosing a flexible curve-fitting like regression
                    model instead of more traditional time series models.<br><br>

                    The Prophet model is eventually fitted using <b>Stan</b> which performs a MAP
                    optimization for the respective parameters. Additionally, this allows for
                    a parameter uncertainty estimation using the Hamiltonian Monte Carlo
                    algorithm.<br><br>

                    <b>Where Prophet performs best</b> Prophet aims to tackle as many usecases in time series forecasting problems as possible. The experience of
                    many Facebook engineers has led to a framework that suffices to model.

                  </p>
                </md-tab>

                <md-tab id="tab-meet-the-team" md-label="Meet the Team">
                  <p>
                    The team behind what if.ai is composed of 9 extraordinary individuals
                    that took time and effort during the extremely demanding COVID-19
                    pandemic to organize and eventually implement a successful model which
                    suffices to predict time series as desired.
                  </p>
                </md-tab>

                <md-tab id="tab-about" md-label="About the Data Sets">
                  <p>
                    
                  </p>
                </md-tab>

                <md-tab id="tab-compare-section" md-label="Compare Section">
                  <p>
                    
                  </p>
                </md-tab>

                <md-tab id="tab-start-predicting" md-label="Start Predicting">
                  <p>

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
