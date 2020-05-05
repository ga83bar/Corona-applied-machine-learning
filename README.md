# Applied Machine Intelligence Project README

## Table of contents
[[_TOC_]]

## Introduction

The overall goal of the project is to make predictions regarding CO2 emissions during the COVID-19 outbreak via predictive modeling.  

## Project ideas

### Overview

We currently have two ideas for the project.  

The first idea focuses on the prediction of future CO2 emissions within a narrow group of comparable countries or regions based on a prediction of future trends in COVID-19 and socioeconomic data.  

The second idea focuses on predicting the impact of COVID-19 on CO2 emissions for countries that are still in the early stages of the COVID-19 pandemic, based on a model trained on comparable countries.  

### Emission predictions based on predicted features

For this approach, we plan to combine data on COVID-19 and socioeconomic factors with past CO2 emission profiles in order to train a model capable of estimating future CO2 emissions.  
We then utilize predicted future trends (such as the future economic development of a country) in order to model the impact of the Corona crisis on CO2 emissions. 
We propose to limit the scope to regions in Germany for now, as the underlying causes for the distribution of various data points may vary by country.  
If deemed feasible and advantageous, we plan on including data from countries whose socioeconomic properties correlate greatly with those of Germany. Likely candidates are Northern European countries.  
Note that data about the development of the pandemic, such as the infection rate, cannot be explicitly implemented as features.  
Instead, they are implicitly included within the predictions of the other features estimated by third parties.  

One advantage of this approach is its potential for interaction by an end user.  
Guided by default predictions, users of the model could enter more pessimistic or optimistic trends to view the impact of varying trends on predicted emissions.  
A web environment lends itself to this approach.  
An early idea of how this might look like can be seen [here](https://www.chartjs.org/).  

A major disadvantage of this proposition is the dependence on accurate predictions of future trends, as well as the potentially inexplicit encoding of key Corona data.  

### Emission developement by country comparison and model adaption

This approach focuses on the adaptation of a model trained on data from countries or regions in the latter stages of the COVID-19 pandemic, 
in order to generate predictions of future CO2 emissions in countries in the early stages of a COVID-19 pandemic.  
The major advantage of this approach lies in the avoidance of predicted future trends in key data.  
The range of responses and infection developments offer the possibility of potentially exploring the immediate impact of different infection scenarios directly.  
However, potential major challenges arise in the model adaption from countries affected early in the pandemic timeline to those affected later on.  
Countries that are currently unaffected may be unaffected because they differ in significant ways from those already hit. One such difference is the degree of industrialization.  
Unaffected countries tend to be non industrialized, and as such their CO2 emissions may react differently to a pandemic than those of an industrialized nation. 
Modeling these differences is difficult because of a lack of data.  

## __FUTURE__

TODO: Future content