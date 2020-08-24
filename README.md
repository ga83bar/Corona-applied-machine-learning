# ML Modeling Progress

## Table of Contents
[[_TOC_]]

## Member Attendances
The following members are on vacation and thus not present:

* Max Putz: 20.8. - 3.9. (not available)
* Aron: 22.9. - 5.9. (still available)

## Quick Summary
This underlying document summarizes measures and ideas for the current ML modeling process which were agreed upon in the first meeting. In particular, it highlightens the **four main categories** as well as the respective **responsible group members**.

## Status
**Next Meeting:** Monday, 24.8. @5pm

## To Do List

### General
- [x] Create an ML Overview Document

### Step 1
- [x] ELM model ready for pipeline
- [ ] Creme model ready for pipeline
- [x] Prophet model ready for pipeline

### Step 2
- [ ] Found best overall model for all data sets
- [ ] Found best model for each individual category (stock, internet traffic, etc.) 

### Step 3
- [ ] Cross-validation data set determined
- [ ] ...

### Step 4
- [ ] Integration parameters defined
- [ ] ...

## 1 Model Architecture Development
In order to catch up on the **clearly failed tasks of Milestone 3**, we compare **three different model approaches** from which we are sure that reasonably good approximations w.r.t. overfitting, etc. are definitely possible.  

The models are all trained and validated on the **four core data sets**:
* Stock Market 
* Internet Exchanges (IX)
* Twitch
* Playstation

This way, we also intend to **compare** different approaches for different data sets, another aspect initially **expected in Milestone 3**.

### 1.1 ELMs
* Responsibility: **Michael Brandner**
* Modeling is pursued using Extreme Learning Machines: [General ELM Architecture](/documentation/Machine Learning Models/MachineLearningModels.md) 

### 1.2 Online Learning 
* Responsibility: **Alexander Griessel**
* Online modeling is pursued using [creme](https://creme-ml.github.io/).

**What is creme?**
>creme is a Python library for online machine learning. All the tools in the library can be updated with a single observation at a time, and can therefore be used to learn from streaming data. This is general-purpose library, and therefore caters to different machine learning problems, including regression, classification, and unsupervised learning.

### 1.3 Time-Series Forecasting 
* Responsibility: **Martin Schuck, Aron Endres**
* Time-series modeling is pursued using [Prophet](https://facebook.github.io/prophet/)

**What is Prophet?**
>Prophet is a procedure for forecasting time series data based on an additive model where non-linear trends are fit with yearly, weekly, and daily seasonality, plus holiday effects. It works best with time series that have strong seasonal effects and several seasons of historical data. Prophet is robust to missing data and shifts in the trend, and typically handles outliers well.
>
>Prophet is open source software released by Facebook’s Core Data Science team. It is available for download on CRAN and PyPI.

## 2 Model Comparison: Data Processing and Parameter Optimization
Essential data processing & preparation regarding things like **time window size**, etc. has to be undergone before any of above models are compared. This way, a somewhat unitary data base is used for comparison. Consequently, model comparison, i.e. parameter optimization, is conducted in order to find the respective best ELM, Online and Prophet models.

* Responsibility: **Henrique Frutuoso**
* The main files to be considered in this step are already pushed, see */res/inference*

## 3 Model Comparison: Cross-Validation
Estimated model outputs need to be cross-validated. The main strategy is still **undetermined and tba**, though every model analyst in *Step 1* is recquired to firstly cross-validate on their own. In *Step 3* we want to **compare** the respective models on a unified cross-validation data set. This way, we can imply - as mentioned above - which model architecture would perform **better (or worse)** for Stock Market, IX, Twitch and Playstation data sets. 

* Responsibility: **Henrique Frutuoso, Aladin Djuhera**

## 4 Integration
In order to **seamlessly integrate** the mathematical models to the web-interface, integration needs to be defined beforehand, i.e. essential parameters such as time windows, etc. need to be communicated. In other words, front- and back-end need to be properly defined and connected. 

* Responsibility: **Niklas Landerer**

## 5 Video
The group project ends with a **promotional video** which introduces the research question, problem set and solution. 

* Responsibility: **Niklas Landerer, Aladin Djuhera**
