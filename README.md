# Blood Glucose Control with [WAT.ai](https://watai.ca/) and [Gluroo Imaginations Inc](https://gluroo.com/).

**ATTENTION**: The work from the Blood Glucose Control team has migrated from this repo to an [organization page](https://github.com/Blood-Glucose-Control) to facilitate more streamlined project management. 

## Causal and Time Series Modeling for Diabetes Management

TPMs: [Christopher Risi](https://github.com/RobotPsychologist), [Walker Payne](https://github.com/walkerpayne), [Dvir Zagury-Grynbaum](https://github.com/dvirzg).

## [Check out our FAQs](https://github.com/RobotPsychologist/bg_control/wiki/Frequently-Asked-Questions)!

Gluroo aims to simplify diabetes management by streamlining the tracking of fitness, nutrition, and insulin use for People with Diabetes (PWD). This project focuses on improving short-term prandial (during meal-time) and postprandial blood glucose level outcomes for people with Type 1 Diabetes (T1D). This complex disease affects nearly 10 million people worldwide. We aim to leverage semi-supervised learning to identify unlabelled meals in time-series blood glucose data, develop meal-scoring functions, and explore causal machine-learning techniques to suggest optimal treatments for user profiles. We aim to provide actionable insights to PWDs and their care practitioners, enhancing health outcomes and quality of life.

## Project Goals

### Phase 1
1. **Meal Identification** develop the ability to identify unlabelled meals in time series BG data. The goal of this project is to be able to identify the top 'n' most significant meals of a PWD per day from continuous glucose monitor data alone. The time series detection models are evaluated on various metrics that measure the proximity of the identified meal regions or change poitns to ground truth labels.

   - **_AI Topics:_** _Feature Engineering, Time Series Annotation, Time Series Representation Learning, Supervised Learning, Semi-Supervised Learning_

### Phase 2

In phase 2 our large team will split off into three sub-teams to work on other diabetes related problems.

1. **Prandial Interventions and Counterfactuals** develop and explore various causal machine learning techniques for estimating the effects of and suggesting pre/postprandial interventions to improve meal scores (uplift modeling, intervention estimations). Develop the ability to provide hindsight (counterfactuals) to PWD, providing interactive experimentation abilities to diabetic care practitioners. This helps PWDs find their personalized best call of action to get intended health results and helps them experiment with different strategies and their direct effects. This is seen in counterfactual estimations as recommendations for better T1D management. E.g. if a user did $X$ during that meal, the glucose response curve would have looked like $Y$.
   - **_AI Topics:_** _Time Series Causal Modelling, Causal Inference, Intervention and Counterfactual Estimation, Causal AI._

2. **Blood Glucose Controller** develop a simulated insulin BG-controller using [open source FDA approved blood glucose control simulators](https://github.com/jxx123/simglucose).
   - **_AI Topics:_** _Representation Learning, Time Series Forecasting, Reinforcement Learning._

3. **Long-range hypoglycemic forecasting** one of the most distressing aspects of living with T1D is the anxiety and fear surrounding [Dead in Bed (DIB) syndrome](https://www.thieme-connect.com/products/ejournals/pdf/10.4103/2321-0656.140880.pdf). Our goal with this project is to provide T1Ds with a long-range glycemic sleep forecast. Strong, practical, and useable results in this space would [significantly impact the diabetes community in relieving diabetes distress](https://journals.sagepub.com/doi/full/10.1177/19322968241267886).
   - **AI Topics**: *Time series Forecasting*

### Phase Future

1. **Meal Scoring** develop the ability to score/evaluate T1D postprandial Blood Glucode Level (BGL) characteristics to serve as a meal-scoring function. Find prandial measures that strongly correlate or predict long-term diabetic health indicators like [Time-in-Range (TIR)](https://jdrf.ca/resources/time-in-range/), [HbA1C%](https://www.breakthrought1d.org/news-and-updates/jdrf-report-how-hba1c-came-1976/), [Glucose Management Indicator](https://diabetesjournals.org/care/article/41/11/2275/36593/Glucose-Management-Indicator-GMI-A-New-Term-for), and [Glucose Variability (GV)](https://journals.lww.com/indjem/fulltext/2013/17040/glycemic_variability__clinical_implications.10.aspx).
   - **_AI Topics:_** _Feature Engineering, Time Series Forecasting, Time Series Representation Learning_


## Background

Diabetes requires a unique way of living. For most, to successfully manage the disease and avoid its long-term adverse effects, you must have detailed fitness and nutrition tracking, not unlike professional athletes or bodybuilders, but with the added complication of knowing how and when to administer insulin. Some can get away without detailed monitoring if they are highly habitual. For most, that’s an undesirable restriction, but where a Person with Diabetes (PWD) falls on that scale is a trade-off that depends on the individual.

At Gluroo, they aim to alleviate PWD's cognitive burden by making fitness, nutrition, and insulin tracking as streamlined as possible. With good tracking and monitoring, the PWD may learn minor behavioural modifications that improve their BG control. Learning these modifications on your own can take months or years of experimentation and often requires waiting months for long meetings with diabetic care professionals to evaluate what changes are necessary. For this project, our aim is to develop tools for improving short-term prandial (meal-time) / postprandial outcomes by providing counterfactuals to PWDs and their diabetic care practitioners.

> improved short-term decisions -> improved long-term disease outcomes

Many things impact a ‘relatively successful’ prandial BG behaviour, the main behavioural ones to focus on tend to be insulin dosing quantity, insulin dosing timing, basal insulin requirements, physical activity (in preceding hours and immediately postprandial), quantity of carbohydrates consumed, glycemic index of carbohydrates consumed, alcohol consumed with meal (slows absorption of carbs), amount of fat and protein consumed with meal (slows absorption of carbs but creates a delayed glucose spike).

If we can provide counterfactuals that improve PWD’s postprandial BG characteristics, we will have made thousands to millions of people’s lives significantly easier and more enjoyable, we will be increasing their freedom to enjoy a wider variety of foods safely, and potentially extending their years living a happy and healthy life.

## Project Timeline

| Month | Milestones |
| :-- | :-- |
| September | Hired a finalized team who want to work on this project |
| October | Team Onboarding, Kick-off Meeting, Initial Model Exploration |
| November | EDA focuses on identifying meals from BG data, and the setup of our MLOps pipelines. |
| December | EDA focus on meal-time scoring metrics, and evaluation of scoring functions in the MLOps pipelines. Writing a substack article summarizing the results of the various meal-time score metrics with visualizations. |
| January | Extensive training runs for causal modelling and time series representation learning. |
| February | Writing up results for publication, soliciting feedback from advisors, multiple drafts and editing. |
| March | Dissemination of results. |
| April | Project wrap-up, next steps and future work, celebration! |
