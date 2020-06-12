# Applied Machine Intelligence Project README

## Table of contents
[[_TOC_]]

## Introduction
The overall goal of this project is to predictively model the impact of the increase in internet traffic due to the COVID-19 outbreak on CO2 emissions.

## Project ideas

### Overview
Utilizing geographically progressions of segmented COVID-19 and internet traffic metrics during the pandemic, a predictive model will be trained with the aim of accurately reproducing the internet traffic related CO2 emission trend over the course of the pandemic. 

The resulting model can be extrapolated to enable CO2 emission prediction in future novel COVID-19 outbreaks, as well as predictions for second-wave outbreaks or future non-COVID-19 pandemics.

### Process
As the goal of the project is to reproduce and predict CO2 emissions due to the change in internet traffic as a result of COVID-19, two approaches must be defined.

1.) The goal of the project is to model the per ton *increase* or percentage *increase* in CO2 emissions

2.) The goal of the project is to model the *total* CO2 emissions

Despite the seemingly trivial difference between these approaches, it is important that data collected and trained with is specifically tailored for each approach. In the first approach, it is a requirement that the training data for internet traffic reflects not the *total* internet traffic at a given point in time, but rather as an *increase* attributal to the COVID-19 pandemic. In the second approach, training data reflects the total internet traffic during the pandemic. However, in the second approach, it is imperative that the model is also trained using data from before the COVID-19 outbreak, as the model should learn to recognize the increase as being attributal to COVID-19.

The major difference then, is that within the first approach, preprocessing of the internet traffic - CO2 emissions relationship is accomplished manually, while in the second approach, the relationship is implcitly encoded into the model. It remains to be seen if human error or model error in regards to this relationship are more likely to impact the performance of the model.

Upon model completion, the model will be offered to a wide audience in the form of an interactive website, where the user can change parametrics of the COVID-19 progression in order to observe the resulting impact on internet-traffic related CO2 emissions.
An early idea of how this might look like can be seen [here](https://www.chartjs.org/).

A key challenge for the success of the model is the reliance on geographic COVID-19 data. Each country employs a differing methodology, as well as differing testing COVID-19 capabilities.

## __CURRENT PROGRESS__

[Team session 09.06.20](/documentation/meeting_transcripts/work_assignment_data.md)