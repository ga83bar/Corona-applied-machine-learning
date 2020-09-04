<div align="center">

# README - What If AI

![alt text](/documentation/Machine%20Learning%20Models/images/logo.png "WhatIfAI")



README for group 11 of the 2020 Applied Machine Intelligence lecture at TUM. 
</div>



[[_TOC_]]

## Short project description
This project aims to quantify the impact that the Covid-19 pandemic has on the global economy, utilising machine learning. One of the main limitations in machine learning is the modelling of unsampled regions in the feature space. Furthermore, models learned during the training process are only valid in the context of unchanged underlying data generation processes. Since the Covid-19 pandemic fundamentally changed the way our society operates, and we don't have any samples of a global pandemic of smaller and/or greater size, it is impossible to directly model the impact of the virus on different branches of the economy. Instead, we aim to model the economy without the pandemic ensuing from January 2020 on. The impact of the pandemic can then be measured as the difference of the predicted courses without Covid-19, and the actual, observed outcomes. The models and its predictions are made accessible with an interactive web interface.


## Requirements

In order to run the project, you need to have Docker and docker-compose installed on your machine. Running the project with Docker takes care of installing the correct project dependencies and environments. 

## How to use

After cloning the directory, you can start the project by running the [docker-compose](/docker-compose.yml) file. This starts both the front- and the backend of our web server. Both docker containers for the front- and backend will build and start up automatically. You can now access the webpage using any browser of your liking at http://localhost:8080/#/.

> **_NOTE:_** Start the docker-compose from the root directory of the project using:
> ```sh
> <user>:~$ docker-compose up
> ```

## File structure

### Data sets
All data sets can be found in the [res](/res) folder. Most Subsets have their own README explaining particular details for this individual set such as the location of related code or comments on the quality.  

> **_NOTE:_** Not all data sets were used in the final project.

### Documentation

The project documentation can be found in the [documentation](/documentation) folder. It includes all milestone reports as well as some meeting transcripts.

### Code base

Our code base is located in the [src](/src) folder. Scrapers, API scripts etc. to obtain raw data can be found in the [data_collection](/src/data_collection) folder. Basic preprocessing and data extraction scripts are located in [data_management](/src/data_management). The unified data preprocessing scripts are saved in [data_pipeline](/src/data_pipeline). The code for training, final model evaluation and live inference for the web interface is located in [inference](/src/inference). Finally, [webinterface](/src/webinterface) contains the code for both front- and backend.  
