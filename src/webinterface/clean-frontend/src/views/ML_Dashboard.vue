<template>
<div class="wrapper">
    <div class="top-pinned">
        <notifications></notifications>
    </div>
    <parallax class="section page-header header-filter" :style="headerStyle"></parallax>
    <div class="main main-raised">
        <div class="section profile-content">

            <div class="container" id="faq">
                <div class="profile-tabs mx-auto">
                    <tabs plain nav-pills-icons color-button="success">
                    </tabs>
                </div>
            </div>

            <div class="container" id="web">
                <h3 class="title">Web Traffic Analysis</h3>
                <div class="md-layout mx-auto fullwidth">
                    <div class="fsize-chart">
                        <line-chart v-if="loaded_graph1" ref="charty" :chartData="chartdata_graph1" :chartLabels="chartlabels_graph1" />
                    </div>
                    <!-- <div v-if="chartdata"> Predicted Class is: {{ chartdata }} yo {{ chartlabels }}</div> -->
                </div>
                <div class="md-layout mx-auto controls">
                    <md-menu md-size="medium" md-align-trigger class="menuu">
                        <md-button md-menu-trigger class="fixed-width-button">{{selectedDataset_graph1}}</md-button>
                        <md-menu-content>
                            <md-menu-item @click="dataset_id='0', selectedDataset_graph1='Internet Exchange Points'">Internet Exchange Points</md-menu-item>
                            <md-menu-item @click="dataset_id='1', selectedDataset_graph1='YouTube Viewchange'">YouTube Viewchange</md-menu-item>
                            <md-menu-item @click="dataset_id='3', selectedDataset_graph1='Steam Users'">Steam Users</md-menu-item>
                            <md-menu-item @click="dataset_id='5', selectedDataset_graph1='Twitch Views'">Twitch Views</md-menu-item>
                            <md-menu-item @click="dataset_id='9', selectedDataset_graph1='PlayStation Network Users'">PlayStation Network Users</md-menu-item>
                        </md-menu-content>
                    </md-menu>
                    <md-button class="md-success md-round run" @click='select_set(1)'>Run Inference</md-button>
                </div>
                <p>
                </p>
            </div>

            <div class="code">
                <div v-if="selectedDataset_graph1=='Internet Exchange Points'">
                    <h4 class="title incode">Internet Exchange Points</h4>
                    In order to accurately depict the trend of an in- or decreasing internet traffic, 
                    data from worldwide exchange points are most representative and given in bitrates per time. <br />
                    <br>
                    These internet exchange points are the physical infrastructure nodes through which Internet Service Providers (ISPs) 
                    such as Deutsche Telekom or Vodafone as well as Content Delivery Networks (CDNs) exchange their internet traffic. As such, 
                    every package worldwide is sent through one of such exchange points. <br />
                    <br />
                    The underlying data set comprises exchange points from Frankfurt, ...
                </div>
            
                <div v-else-if="selectedDataset_graph1=='YouTube Views'">
                    <h4 class="title incode">YouTube Views</h4>
                    No text
                </div>

                <div v-else-if="selectedDataset_graph1=='Steam Users'">
                    <h4 class="title incode">Steam Network Users</h4>
                    Online gaming has seen a surge during the COVID-19 pandemic on several platforms. <br />
                    <br />
                    The underlying "Steam Network Users" data set describes the network activity (i.e. currently active users) 
                    on the Steam gaming platform for the respective timeline. 
                </div>

                <div v-else-if="selectedDataset_graph1=='Twitch Views'">
                    <h4 class="title incode">Twitch Viewtime</h4>
                    During the COVID-19 pandemic, internet streaming has greatly increased.
                    The currently most popular streaming platform Twitch thus suffices to
                    provide data for a time-series forecast.<br><br>

                    The underlying ”Twitch Views” data set describes the viewcount for the
                    respective streams on the platform. The data was obtained by scraping
                    through Twitch analytics using a custom build Twitch scraper.
                </div>

                <div v-else-if="selectedDataset_graph1=='PlayStation Network Users'">
                    <h4 class="title incode">PlayStation Network Users</h4>
                    Online gaming has seen a surge during the COVID-19 pandemic on several
                    platforms.<br><br>
                    The underlying ”PlayStation Network Users” data set describes the network activity (i.e. currently active users) on Sony PlayStation consoles
                    for the respective timeline.
                </div>
                
                <div v-else>
                    <h4 class="title incode">No dataset selected yet</h4>
                </div>
            </div>

            <div class="container" id="stock">
                <h3 class="title">Stock Predictions</h3>
                <div class="md-layout mx-auto fullwidth">
                    <div class="fsize-chart">
                        <line-chart v-if="loaded_graph2" ref="charty" :chartData="chartdata_graph2" :chartLabels="chartlabels_graph2" />
                    </div>
                    <!-- <div v-if="chartdata"> Predicted Class is: {{ chartdata }} yo {{ chartlabels }}</div> -->
                </div>
                <div class="md-layout mx-auto controls">
                    <md-menu md-size="medium" md-align-trigger class="menuu">
                        <md-button md-menu-trigger class="fixed-width-button">{{selectedDataset_graph2}}</md-button>
                        <md-menu-content>
                            <md-menu-item @click="dataset_id='10', selectedDataset_graph2='Medical Stock'">Medical Stock</md-menu-item>
                            <md-menu-item @click="dataset_id='11', selectedDataset_graph2='Banking Stock'">Banking Stock</md-menu-item>
                            <md-menu-item @click="dataset_id='12', selectedDataset_graph2='Energy Stock'">Energy Stock</md-menu-item>
                            <md-menu-item @click="dataset_id='13', selectedDataset_graph2='Oil Stock'">Oil Stock</md-menu-item>
                            <md-menu-item @click="dataset_id='14', selectedDataset_graph2='Steel Stock'">Steel Stock</md-menu-item>
                            <md-menu-item @click="dataset_id='15', selectedDataset_graph2='Automotive Stock'">Automotive Stock</md-menu-item>
                            <md-menu-item @click="dataset_id='16', selectedDataset_graph2='Telecom Stock'">Telecom Stock</md-menu-item>
                            <md-menu-item @click="dataset_id='17', selectedDataset_graph2='Tech Stock'">Tech Stock</md-menu-item>
                        </md-menu-content>
                    </md-menu>
                    <md-button class="md-success md-round run" @click='select_set(2)'>Run Inference</md-button>
                </div>

            </div>

            <div class="code">
                <div v-if="selectedDataset_graph2=='Medical Stock'">
                    <h4 class="title incode">Medical Stock</h4>
                    The COVID-19 pandemic has had and still has a great influence on the
                    global stock market. In order to analyze its effect, stocks within a specified time range can be analyzed.<br><br>

                    The underlying ”Medical Stock” data set comprises a feature set of the
                    currently most important medical tech companies. In particular, these are<br><br>

                    (a) Evotec AG<br>
                    (b) Siemens Healthineers AG<br>
                    (c) ...
                </div>

                <div v-if="selectedDataset_graph2=='Banking Stock'">
                    <h4 class="title incode">Banking Stock</h4>
                    The COVID-19 pandemic has had and still has a great influence on the
                    global stock market. In order to analyze its effect, stocks within a specified time range can be analyzed.<br><br>

                    The underlying ”Banking Stock” data set comprises a feature set of the
                    currently most important financial institutions listed in the worldwide
                    stock indexes. In particular, these are<br><br>

                    (a) Deutsche Bank<br>
                    (b) Goldman Sachs<br>
                    (c) ...
                </div>

                <div v-if="selectedDataset_graph2=='Energy Stock'">
                    <h4 class="title incode">Energy Stock</h4>
                    The COVID-19 pandemic has had and still has a great influence on the
                    global stock market. In order to analyze its effect, stocks within a specified time range can be analyzed.<br><br>
                    
                    The underlying ”Energy Stock” data set comprises a feature set of the
                    currently most important companies with a focus in energy and electricity
                    operation listed in the worldwide stock indexes. In particular, these are<br><br>

                    (a) Siemens AG<br>
                    (b) Duke Energy Corporation<br>
                    (c) ...
                </div>

                <div v-if="selectedDataset_graph2=='Oil Stock'">
                    <h4 class="title incode">Oil Stock</h4>
                    The COVID-19 pandemic has had and still has a great influence on the
                    global stock market. In order to analyze its effect, stocks within a specified time range can be analyzed.<br><br>
                    
                    The underlying ”Oil Stock” data set comprises a feature set of the currently most important companies operating in the field of oil production.
                    In particular, these are<br><br>

                    (a) Shell<br>
                    (b) ExxonMobil<br>
                    (c) ...
                </div>

                <div v-if="selectedDataset_graph2=='Steel Stock'">
                    <h4 class="title incode">Steel Stock</h4>
                    The COVID-19 pandemic has had and still has a great influence on the
                    global stock market. In order to analyze its effect, stocks within a specified time range can be analyzed.<br><br>
                    
                    The underlying ”Steel Stock” data set comprises a feature set of the currently most important companies operating in the field of steel production.
                    In particular, these are<br><br>

                    (a) ThyssenKrupp AG<br>
                    (b) ArcelorMittal S.A.<br>
                    (c) ...
                </div>

                <div v-if="selectedDataset_graph2=='Automotive Stock'">
                    <h4 class="title incode">Automotive Stock</h4>
                    The COVID-19 pandemic has had and still has a great influence on the
                    global stock market. In order to analyze its effect, stocks within a specified time range can be analyzed.<br><br>
                    
                    The underlying ”Automotive Stock” data set comprises a feature set of
                    the currently most important automitive companies. In particular, these
                    are<br><br>

                    (a) BMW<br>
                    (b) Toyota<br>
                    (c) ...
                </div>

                <div v-if="selectedDataset_graph2=='Telecom Stock'">
                    <h4 class="title incode">Telecom Stock</h4>
                    The COVID-19 pandemic has had and still has a great influence on the
                    global stock market. In order to analyze its effect, stocks within a specified time range can be analyzed.<br><br>
                    
                    The underlying ”Telecom Stock” data set comprises a feature set of the
                    currently most important telecom companies. In particular, these are<br><br>

                    (a) ATT<br>
                    (b) Verizon<br>
                    (c) ...
                </div>

                <div v-if="selectedDataset_graph2=='Tech Stock'">
                    <h4 class="title incode">Tech Stock</h4>
                    The COVID-19 pandemic has had and still has a great influence on the
                    global stock market. In order to analyze its effect, stocks within a specified time range can be analyzed.<br><br>
                    
                    The underlying ”Tech Stock” data set comprises a feature set of the currently most important tech companies. In particular, these are<br><br>

                    (a) Apple<br>
                    (b) Huawei<br>
                    (c) ...
                </div>

                <div v-else>
                    <h4 class="title incode">No dataset selected yet</h4>
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
            loaded_graph1: false,
            loaded_graph2: false,
            connection: false,
            start_date: format(now, dateFormat),
            end_date: format(now, dateFormat),
            selectedDataset_graph1: 'Select dataset',
            selectedDataset_graph2: 'Select dataset',
            disabledDates: function (date) {
                // compare if today is greater then the datepickers date
            },
            dataset_id: '1',
            chartdata: null,
            chartlabels: null,
            datecheck_bool: null,
            chart: {
                responsive: true,
                maintainAspectRatio: true,
                aspectRatio: 2
            },
            options: {
                showScale: true,
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: false,
                            callback: (value, index, values) => {
                                return this.formatNumber(value)
                            }
                        },
                        gridLines: {
                            display: true,
                            color: '#EEF0F4',
                            borderDash: [5, 15]
                        }
                    }],
                    xAxes: [{
                        gridLines: {
                            display: true,
                            color: '#EEF0F4',
                            borderDash: [5, 15]
                        }
                    }]
                },
                tooltips: {
                    backgroundColor: '#4F5565',
                    titleFontStyle: 'normal',
                    titleFontSize: 18,
                    bodyFontFamily: "'Proxima Nova', sans-serif",
                    cornerRadius: 3,
                    bodyFontColor: '#20C4C8',
                    bodyFontSize: 14,
                    xPadding: 14,
                    yPadding: 14,
                    displayColors: false,
                    mode: 'index',
                    intersect: false,
                    callbacks: {
                        title: tooltipItem => {
                            return `🗓 ${tooltipItem[0].xLabel}`
                        },
                        label: (tooltipItem, data) => {
                            let dataset = data.datasets[tooltipItem.datasetIndex]
                            let currentValue = dataset.data[tooltipItem.index]
                            return `📦 ${currentValue.toLocaleString()}`
                        }
                    }
                },
                responsive: true,
                maintainAspectRatio: false
            }

        }
    },
    computed: {
        // eslint-disable-next-line

        dateFormat() {
            return this.$material.locale.dateFormat || 'yyyy-MM-dd'
        }
    },

    methods: {

        ping_server() {
            axios.post('http://localhost:5000/predict', {
                    ping: 1
                })
                .then(response => {

                    if (response.data.alive === 1) {
                        this.connection = true;
                        this.notifyVue('top', 'center', 'success', 'Connection to backend established.');

                    } else {
                        this.connection = false;
                        this.notifyVue('top', 'center', 'danger', 'Backend is not configured properly.');
                    }

                })
                .catch(e => {
                    this.notifyVue('top', 'center', 'danger', 'Connection failed. Backend is not responding.');

                })
        },

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
        select_set(selected_graph) {

            if(selected_graph == 1){
                this.loaded_graph1 = false;
            }
            else{
                this.loaded_graph2 = false;
            }
            
            axios.post('http://localhost:5000/predict', {
                    dataset_id_req: this.dataset_id,
                    selected_graph: selected_graph
                })
                .then(response => {

                    
                        this.acceptedRequest = response.data.class;
                        if( response.data.selected_graph == 1)
                        {
                            this.chartlabels_graph1 = response.data.labels,
                            this.chartdata_graph1 = [{
                                    label: 'real data',
                                    data: response.data.chart_data_1,
                                    borderColor: 'rgb(0, 0, 0)',
                                    fill: false
                                },
                                {
                                    label: 'model data',
                                    data: response.data.chart_data_2,
                                    borderColor: 'rgb(112, 112, 112)',
                                    fill: false
                                },
                                {
                                    label: 'prediction',
                                    data: response.data.chart_data_3,
                                    borderColor: 'rgb(255, 0, 0)',
                                    fill: false
                                }
                            ]
                        }

                        else if( response.data.selected_graph == 2)
                        {
                            this.chartlabels_graph2 = response.data.labels,
                            this.chartdata_graph2 = [{
                                    label: 'real data',
                                    data: response.data.chart_data_1,
                                    borderColor: 'rgb(0, 0, 0)',
                                    fill: false
                                },
                                {
                                    label: 'model data',
                                    data: response.data.chart_data_2,
                                    borderColor: 'rgb(112, 112, 112)',
                                    fill: false
                                },
                                {
                                    label: 'prediction',
                                    data: response.data.chart_data_3,
                                    borderColor: 'rgb(255, 0, 0)',
                                    fill: false
                                }
                            ]
                        }
                        
                        this.datecheck_bool = response.data.datecheck;
                        if(selected_graph == 1){
                            this.loaded_graph1 = true;
                        }
                        else{
                            this.loaded_graph2 = true;
                        }
                        this.checkdate(this.datecheck_bool);
                })
                .catch(e => {
                    this.notifyVue('top', 'center', 'danger', 'Connection failed.');
                })

        },
        toString() {
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
        checkdate(bool) {
            if (bool == 1) {
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
        }

    },
    mounted() {
        //executed after page is loaded -> see vue component lifeciycle
        this.ping_server();
        this.select_set();

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

.menuu {
    margin-right: 5em;
    margin-top: 0.15em;
}

.code {
    background: rgb(40, 44, 52);
    color: #fff;
    margin: 2em;
    padding: 2em;
    border-radius: 0.4em;
    webkit-box-shadow: 0px 0px 25px 0px rgba(0, 0, 0, 0.39);
    -moz-box-shadow: 0px 0px 25px 0px rgba(0, 0, 0, 0.39);
    box-shadow: 0px 0px 25px 0px rgba(0, 0, 0, 0.39);
}

.incode {
    color: #fff;
    margin-top: 0;
}

.main-raised {
    max-width: 1200px;
    margin-left: auto;
    margin-right: auto;
}

.controls {
    margin-top: 50px;
    margin-bottom: 10px;

}

/* chart */

.top-pinned {
    position: fixed;
    width: 100%;
    top: 0;
    z-index: 9000;
    background: transparent
}

/* page */
.profile-page {
    .page-header {
        height: 180px;
        background-position: center center;

        &::before {
            background: rgba(0, 0, 0, .2);
        }
    }

}

.fsize-chart {
    margin-top: 35px;
    width: 100%;
}

.fullwidth {
    width: 100%
}

.fixed-width-button {
    width: 16em;
}
</style>
