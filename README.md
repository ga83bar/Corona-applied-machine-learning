# Applied Machine Intelligence Project README

[[_TOC_]]

## Introduction

The overall goal of the project is to make predictions regarding CO2 emissions during the COVID-19 outbreak via predictive modeling. 

## Project ideas

### Overview

We currently have two ideas for the project. The first one focusses on the prediction of future CO2 emissions within a narrow group of comparable countries based on predicted features. The second one focusses on making predictions for countries that are still in the early stages of the COVID pandemic by applying a model trained on comparable countries.

### Emission predictions based on predicted features

For this approach, we plan to use several features and past CO2 emission profiles in order to train a model that estimates the CO2 emissions based on these features. We then use predictions of the features such as the future economic development of a country to model the impact of the Corona crisis. In order to account for country-based differences in the relationship of features, we propose to limit the scope to Germany at first. If deemed feasible and advantageous, we plan on including data from countries that share a large portion of the social and economical properties with Germany such as other northern european countries. Note that data about the development of the pandemic such as the infection rate is not explicitly contained as features, but implicitly within other features estimated by third parties.

One advantage of this approach is its interactive potential. Based on the default future feature development prediction, users of the model could enter more pessimistic/optimistic trends in a web environment to view its impact on the predicted emissions. An early idea how this might look like can be seen [here](https://www.chartjs.org/)

A major disadvantage is its dependency on solid predictions for its features, as well as the non-explicit inclusion of Corona key figures.

### Emission developement by country comparison and model adaption

This approach focusses on the adaption of a model trained on countries/regions that are already far into the pandemic to make predictions for countries currently still less affected. The major advantage here is that one could potentially bypass the prediction of model features. Because of the range of responses and infection developments, it could also be possible to explore the direct impact of different infection scenarios directly. Major challenges arise in the model adaption however. Countries that are currently unaffected are mostly non industrialized and as such might behave fundamentally different during the pandemic. Modeling these differences is also hardly possible because there is no data on such situations.

## __FUTURE__

TODO: Future content