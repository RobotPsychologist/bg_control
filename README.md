# Blood Glucose Control with Wat.ai and Gluroo

## Causal Modeling and Time Series Representation Learning for Diabetes Management

TPMs: [Christopher Risi](https://github.com/RobotPsychologist), [Walker Payne](https://github.com/walkerpayne), Dvir Zagury-Grynbaum

Gluroo aims to simplify diabetes management by streamlining the tracking of fitness, nutrition, and insulin use for people with diabetes (PWD). This project focuses on improving short-term prandial (meal-time) and postprandial blood glucose outcomes for people with type 1 diabetes, a complex disease that affects nearly 10 million people worldwide. We aim to leverage semi-supervised learning to identify unlabelled meals in time-series blood glucose data, develop meal-scoring functions, and explore causal machine-learning techniques. Our goal is to provide actionable insights to PWD and their care practitioners, enhancing health outcomes and quality of life.

## Project Goals

1. **Meal Identification** develop the ability to identify unlabelled meals in time series BG data. 
    - ***AI Topics:*** *Feature Engineering, Time Series Representation Learning*

2. **Meal Scoring** develop the ability to score/evaluate T1D postprandial BGL characteristics to serve as a meal-scoring function. Find prandial measures that strongly correlate or predict long-term diabetic health indicators like [Time-in-Range (TIR)](https://jdrf.ca/resources/time-in-range/), [HbA1C%](https://www.breakthrought1d.org/news-and-updates/jdrf-report-how-hba1c-came-1976/), [Glucose Management Indicator](https://diabetesjournals.org/care/article/41/11/2275/36593/Glucose-Management-Indicator-GMI-A-New-Term-for), and [Glucose Variability (GV)](https://journals.lww.com/indjem/fulltext/2013/17040/glycemic_variability__clinical_implications.10.aspx). 
    - ***AI Topics:*** *Feature Engineering, Time Series Forecasting, Time Series Representation Learning*
3. **Prandial Interventions and Counterfactuals** Develop and explore various causal machine learning techniques for reasoning about pre/postprandial interventions to improve meal scores (uplift modeling, intervention estimations). Develop the ability to provide hindsight (counterfactuals) to PWD that can offer coaching tools to diabetic care practitioners.
Generate counterfactual suggestions as coaching tools for T1D management based on above data features. E.g. if you did $X$ during this meal, the glucose response curve would look like $Y$.
    - ***AI Topics:*** *Time Series Forecasting + Causal Modeling.*

4. **Blood Glucose Controller** develop a simulated insulin BG-controller using [open source FDA approved blood glucose control simulators](https://github.com/jxx123/simglucose). 
   -    ***AI Topics:*** *Representation Learning, Time Series Forecasting, Reinforcement Learning.*



## Background

Diabetes requires a unique way of living. For most, to successfully manage the disease and avoid its long-term adverse effects, you must have detailed fitness and nutrition tracking, not unlike professional athletes or bodybuilders, but with the added complication of knowing how and when to administer insulin. Some can get away without detailed monitoring if they are highly habitual. For most, that’s an undesirable restriction, but where a Person with Diabetes (PWD) falls on that scale is a trade-off that depends on the individual. 
	
At Gluroo, they aim to alleviate PWD's cognitive burden by making fitness, nutrition, and insulin tracking as streamlined as possible. With good tracking and monitoring, the PWD may learn minor behavioural modifications that improve their BG control. Learning these modifications on your own can take months or years of experimentation and often requires waiting months for long meetings with diabetic care professionals to evaluate what changes are necessary. For this project, our aim is to develop tools for improving short-term prandial (meal-time) / postprandial outcomes by providing counterfactuals to PWDs and their diabetic care practitioners. 

> improved short-term decisions -> improved long-term disease outcomes

Many things impact a ‘relatively successful’ prandial BG behaviour, the main behavioural ones to focus on tend to be insulin dosing quantity, insulin dosing timing, basal insulin requirements, physical activity (in preceding hours and immediately postprandial), quantity of carbohydrates consumed, glycemic index of carbohydrates consumed, alcohol consumed with meal (slows absorption of carbs), amount of fat and protein consumed with meal (slows absorption of carbs but creates a delayed glucose spike). 

If we can provide counterfactuals that improve PWD’s postprandial BG characteristics, we will have made thousands to millions of people’s lives significantly easier and more enjoyable, we will be increasing their freedom to enjoy a wider variety of foods safely, and potentially extending their years living a happy and healthy life.


### Interesting Papers

#### 1. Diabetes Management
##### Meal Identification / Anomaly Detection
- [Data-Driven Blood Glucose Pattern Classification and Anomalies Detection: Machine-Learning Applications in Type 1 Diabetes](https://pubmed.ncbi.nlm.nih.gov/31042157/)
- [Identification of the Optimal Meal Detection Strategy for Adults, Adolescents, and Children with Type 1 Diabetes: an in Silico Validation](https://ieeexplore.ieee.org/document/10197041)
- [An LSTM-based Approach Towards Automated Meal Detection from Continuous Glucose Monitoring in Type 1 Diabetes Mellitus | IEEE Conference Publication](https://ieeexplore.ieee.org/document/9635246)
- [Automated meal detection from continuous glucose monitor data through simulation and explanation](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6857509/)
#### 2. Time-Series Representation Learning
- 
#### 3. Causal Modelling


## Project Timeline

|Month | Milestones | 
| - | :- |
|September | Hired a finalized team who want to work on this project |
| October | Team Onboarding, Diabetes Workshop, Time-Series + Causal Modeling Workshop, Github + MLOps Training, outline of modelling pipeline. |
| November | EDA focuses on identifying meals from BG data, and the setup of our MLOps pipeline. |
| December | EDA focus on meal-time scoring metrics, and evaluation of scoring functions in the MLOps pipeline. Writing a substack article summarizing the results of the various meal-time score metrics with visualizations. |
| January | Extensive training runs for causal modelling and time series representation learning. |
| February | Writing up results for publication, soliciting feedback from advisors, multiple drafts and editing. |
| March | Dissemination of results. |
| April | Project wrap-up, next steps and future work, celebration!
|

 

 



 

 

 

 

 





## About Us - Short Bios

### Technical Project Managers:
#### Christopher Risi
[Christopher Risi](https://www.linkedin.com/in/christopherrisi/) is a computer science PhD student at the University of Waterloo specializing in artificial intelligence. He works in the University of Waterloo's [Computational Health Informatics Lab (CHIL)](https://chil.uwaterloo.ca/) and as a Consultant, AI Research and Health Insights at [Gluroo Imaginations Inc](https://gluroo.com/). Christopher's research focuses on finding ways to utilize a wide variety of AI tools for easing and improving diabetes management. Christopher has Latent Autoimmune Diabetes of Adults (LADA) a subtype of T1D.


#### Walker Payne

#### Dvir Zagury-Grynbaum

### Core Members:

#### TBD 1

#### TBD 2

#### TBD [...]