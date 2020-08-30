<template>
<div class="wrapper">
    <div class="top-pinned">
        <notifications></notifications>
    </div>
    <parallax class="section page-header header-filter" :style="headerStyle"></parallax>
    <div class="main main-raised">
        <div class="section profile-content">

            <div class="container" id="stock">
                <h3 class="title">Stock Predictions</h3>
                <div class="md-layout mx-auto fullwidth">
                    <div class="fsize-chart">
                        <line-chart v-if="loaded" ref="charty" :chartData="chartdata_graph1" :chartLabels="chartlabels_graph1" />
                    </div>
                    <!-- <div v-if="chartdata"> Predicted Class is: {{ chartdata }} yo {{ chartlabels }}</div> -->
                </div>
                <div class="md-layout mx-auto controls">
                    <md-menu md-size="medium" md-align-trigger class="menuu">
                        <md-button md-menu-trigger class="fixed-width-button">{{selectedDataset}}</md-button>
                        <md-menu-content>
                            <md-menu-item @click="model='1', selectedDataset='Stock A'">Stock A</md-menu-item>
                            <md-menu-item @click="model='2', selectedDataset='Stock B'">Stock B</md-menu-item>
                            <md-menu-item @click="model='3', selectedDataset='Stock C'">Stock C</md-menu-item>
                        </md-menu-content>
                    </md-menu>
                    <md-button class="md-success md-round run" @click='select_set(1)'>Run Inference</md-button>
                </div>
                <p>
                </p>
            </div>

            <div class="code">
                <h4 class="title incode">Quick and Simple Description</h4>
                Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.
            </div>

            <div class="container" id="web">
                <h3 class="title">Web Traffic Analysis</h3>
                <div class="md-layout mx-auto fullwidth">
                    <div class="fsize-chart">
                        <line-chart v-if="loaded" ref="charty" :chartData="chartdata_graph2" :chartLabels="chartlabels_graph2" />
                    </div>
                    <!-- <div v-if="chartdata"> Predicted Class is: {{ chartdata }} yo {{ chartlabels }}</div> -->
                </div>
                <div class="md-layout mx-auto controls">
                    <md-menu md-size="medium" md-align-trigger class="menuu">
                        <md-button md-menu-trigger class="fixed-width-button">{{selectedDataset}}</md-button>
                        <md-menu-content>
                            <md-menu-item @click="model='1', selectedDataset='Stock A'">Stock A</md-menu-item>
                            <md-menu-item @click="model='2', selectedDataset='Stock B'">Stock B</md-menu-item>
                            <md-menu-item @click="model='3', selectedDataset='Stock C'">Stock C</md-menu-item>
                        </md-menu-content>
                    </md-menu>
                    <md-button class="md-success md-round run" @click='select_set(2)'>Run Inference</md-button>
                </div>

            </div>

            <div class="code">
                <h4 class="title incode">Corona has taken porn consumption to a new level </h4>
                Obviously, this is placeholder content. Also, I am fluent in Latin.<br />Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.
            </div>
            <div class="container" id="faq">
                <div class="profile-tabs mx-auto">
                    <tabs plain nav-pills-icons color-button="success">
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
            loaded: false,
            connection: false,
            start_date: format(now, dateFormat),
            end_date: format(now, dateFormat),
            selectedDataset: 'Select dataset',
            disabledDates: function (date) {
                // compare if today is greater then the datepickers date
            },
            model: '1',
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

            this.loaded = false;
            axios.post('http://localhost:5000/predict', {
                    dataset_id_req: this.model,
                    selected_graph: selected_graph
                })
                .then(response => {

                    
                        this.acceptedRequest = response.data.class;
                        if( response.data.selected_graph == 1)
                        {
                            this.chartlabels_graph1 = response.data.labels,
                            this.chartdata_graph1 = [{
                                    label: 'deaths',
                                    data: response.data.chart_data_1,
                                    borderColor: 'rgb(238, 76, 96)',
                                    fill: false
                                },
                                {
                                    label: 'cases',
                                    data: response.data.chart_data_2,
                                    borderColor: 'rgb(76, 175, 80)',
                                    fill: false
                                }
                            ]
                        }

                        else if( response.data.selected_graph == 2)
                        {
                            this.chartlabels_graph2 = response.data.labels,
                            this.chartdata_graph2 = [{
                                    label: 'test1',
                                    data: response.data.chart_data_1,
                                    borderColor: 'rgb(238, 76, 96)',
                                    fill: false
                                },
                                {
                                    label: 'cases',
                                    data: response.data.chart_data_2,
                                    borderColor: 'rgb(76, 175, 80)',
                                    fill: false
                                }
                            ]
                        }
                        
                        this.datecheck_bool = response.data.datecheck,
                            this.loaded = true,
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
    width: 12em;
}
</style>
