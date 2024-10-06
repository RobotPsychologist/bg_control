# Blood Glucose Control with [WAT.ai](https://watai.ca/) and [Gluroo Imaginations Inc](https://gluroo.com/).

## Causal Modeling and Time Series Representation Learning for Diabetes Management

TPMs: [Christopher Risi](https://github.com/RobotPsychologist), [Walker Payne](https://github.com/walkerpayne), [Dvir Zagury-Grynbaum](https://github.com/dvirzg).

## [Check out our FAQs](https://github.com/RobotPsychologist/bg_control/wiki/Frequently-Asked-Questions)!

Gluroo aims to simplify diabetes management by streamlining the tracking of fitness, nutrition, and insulin use for People with Diabetes (PWD). This project focuses on improving short-term prandial (during meal-time) and postprandial blood glucose level outcomes for people with Type 1 Diabetes (T1D). This complex disease affects nearly 10 million people worldwide. We aim to leverage semi-supervised learning to identify unlabelled meals in time-series blood glucose data, develop meal-scoring functions, and explore causal machine-learning techniques to suggest optimal treatments for user profiles. We aim to provide actionable insights to PWDs and their care practitioners, enhancing health outcomes and quality of life.

## Project Goals

1. **Meal Identification** develop the ability to identify unlabelled meals in time series BG data.

   - **_AI Topics:_** _Feature Engineering, Time Series Representation Learning_

2. **Meal Scoring** develop the ability to score/evaluate T1D postprandial Blood Glucode Level (BGL) characteristics to serve as a meal-scoring function. Find prandial measures that strongly correlate or predict long-term diabetic health indicators like [Time-in-Range (TIR)](https://jdrf.ca/resources/time-in-range/), [HbA1C%](https://www.breakthrought1d.org/news-and-updates/jdrf-report-how-hba1c-came-1976/), [Glucose Management Indicator](https://diabetesjournals.org/care/article/41/11/2275/36593/Glucose-Management-Indicator-GMI-A-New-Term-for), and [Glucose Variability (GV)](https://journals.lww.com/indjem/fulltext/2013/17040/glycemic_variability__clinical_implications.10.aspx).
   - **_AI Topics:_** _Feature Engineering, Time Series Forecasting, Time Series Representation Learning_
3. **Prandial Interventions and Counterfactuals** develop and explore various causal machine learning techniques for estimating the effects of and suggesting pre/postprandial interventions to improve meal scores (uplift modeling, intervention estimations). Develop the ability to provide hindsight (counterfactuals) to PWD, providing interactive experimentation abilities to diabetic care practitioners. This helps PWDs find their personalized best call of action to get intended health results and helps them experiment with different strategies and their direct effects. This is seen in counterfactual estimations as recommendations for better T1D management. E.g. if a user did $X$ during that meal, the glucose response curve would have looked like $Y$. - **_AI Topics:_** _Time Series Causal Modelling, Causal Inference, Intervention and Counterfactual Estimation, Causal AI._

4. **Blood Glucose Controller** develop a simulated insulin BG-controller using [open source FDA approved blood glucose control simulators](https://github.com/jxx123/simglucose).
   - **_AI Topics:_** _Representation Learning, Time Series Forecasting, Reinforcement Learning._

5. **Long-range hypoglycemic forecasting** one of the most distressing aspects of living with T1D is the anxiety and fear surrounding [Dead in Bed (DIB) syndrome](https://www.thieme-connect.com/products/ejournals/pdf/10.4103/2321-0656.140880.pdf). Our goal with this project is to provide T1Ds with a long-range glycemic sleep forecast. Strong, practical, and useable results in this space would [significantly impact the diabetes community in relieving diabetes distress](https://journals.sagepub.com/doi/full/10.1177/19322968241267886). 


## Background

Diabetes requires a unique way of living. For most, to successfully manage the disease and avoid its long-term adverse effects, you must have detailed fitness and nutrition tracking, not unlike professional athletes or bodybuilders, but with the added complication of knowing how and when to administer insulin. Some can get away without detailed monitoring if they are highly habitual. For most, that’s an undesirable restriction, but where a Person with Diabetes (PWD) falls on that scale is a trade-off that depends on the individual.

At Gluroo, they aim to alleviate PWD's cognitive burden by making fitness, nutrition, and insulin tracking as streamlined as possible. With good tracking and monitoring, the PWD may learn minor behavioural modifications that improve their BG control. Learning these modifications on your own can take months or years of experimentation and often requires waiting months for long meetings with diabetic care professionals to evaluate what changes are necessary. For this project, our aim is to develop tools for improving short-term prandial (meal-time) / postprandial outcomes by providing counterfactuals to PWDs and their diabetic care practitioners.

> improved short-term decisions -> improved long-term disease outcomes

Many things impact a ‘relatively successful’ prandial BG behaviour, the main behavioural ones to focus on tend to be insulin dosing quantity, insulin dosing timing, basal insulin requirements, physical activity (in preceding hours and immediately postprandial), quantity of carbohydrates consumed, glycemic index of carbohydrates consumed, alcohol consumed with meal (slows absorption of carbs), amount of fat and protein consumed with meal (slows absorption of carbs but creates a delayed glucose spike).

If we can provide counterfactuals that improve PWD’s postprandial BG characteristics, we will have made thousands to millions of people’s lives significantly easier and more enjoyable, we will be increasing their freedom to enjoy a wider variety of foods safely, and potentially extending their years living a happy and healthy life.

### Interesting Background Papers and Links

#### 1. Diabetes Management

##### Meal Identification / Anomaly Detection

- [Data-Driven Blood Glucose Pattern Classification and Anomalies Detection: Machine-Learning Applications in Type 1 Diabetes](https://pubmed.ncbi.nlm.nih.gov/31042157/)
- [Identification of the Optimal Meal Detection Strategy for Adults, Adolescents, and Children with Type 1 Diabetes: an in Silico Validation](https://ieeexplore.ieee.org/document/10197041)
- [An LSTM-based Approach Towards Automated Meal Detection from Continuous Glucose Monitoring in Type 1 Diabetes Mellitus](https://ieeexplore.ieee.org/document/9635246)
- [Automated meal detection from continuous glucose monitor data through simulation and explanation](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6857509/)

##### Insulin Bolus Timing

- [Insulearn](http://ddi.ucsd.edu/insulearn/terminology.html)

#### 2. Time-Series Representation Learning

- [Universal Time-Series Representation Learning: A Survey](https://arxiv.org/pdf/2401.03717)

#### 3. Causal Modelling

- [Causal Machine Learning: A Survey and Open Problems](https://arxiv.org/pdf/2206.15475)
- [Causality - Judea Pearl ](https://bayes.cs.ucla.edu/BOOK-2K/) (Causal Inference textbook gold standard, long read).

#### 4. Time Series + Causal Modeling

- [Causal inference for time series analysis: problems, methods and evaluation ](https://link.springer.com/article/10.1007/s10115-021-01621-0)
- [Survey and Evaluation of Causal Discovery Methods for Time Series ](https://www.jair.org/index.php/jair/article/view/13428)
- [Causal inference for time series](https://www.nature.com/articles/s43017-023-00431-y)
- [A Survey of Deep Causal Models and Their Industrial Applications](https://arxiv.org/pdf/2209.08860)
- [Causal Inference with Time-Series Cross-Sectional Data: A Reflection](https://papers.ssrn.com/sol3/Papers.cfm?abstract_id=3979613)

#### 5. Reinforcement Learning for Blood Glucose Control
- [Deep Reinforcement Learning for Closed-Loop Blood Glucose Control](http://proceedings.mlr.press/v126/fox20a/fox20a.pdf)

#### 6. Nocturnal Hypoglycemic Forecasting
- [Fear of Hypoglycemia and Diabetes Distress: Expected Reduction by Glucose Prediction](https://journals.sagepub.com/doi/full/10.1177/19322968241267886)


## Project Timeline

| Month | Milestones |
| :-- | :-- |
| September | Hired a finalized team who want to work on this project |
| October | Team Onboarding, Diabetes Workshop, Time-Series + Causal Modeling Workshop, Github + MLOps Training, outline of modeling pipeline. |
| November | EDA focuses on identifying meals from BG data, and the setup of our MLOps pipelines. |
| December | EDA focus on meal-time scoring metrics, and evaluation of scoring functions in the MLOps pipelines. Writing a substack article summarizing the results of the various meal-time score metrics with visualizations. |
| January | Extensive training runs for causal modelling and time series representation learning. |
| February | Writing up results for publication, soliciting feedback from advisors, multiple drafts and editing. |
| March | Dissemination of results. |
| April | Project wrap-up, next steps and future work, celebration! |

## About Us - Short Bios

:syringe: :droplet: = T1D

### Technical Project Managers:

#### Christopher Risi :syringe: :droplet:

[Christopher Risi](https://www.linkedin.com/in/christopherrisi/) is a computer science PhD student at the University of Waterloo specializing in artificial intelligence. He works in the University of Waterloo's [Computational Health Informatics Lab (CHIL)](https://chil.uwaterloo.ca/) and as a Consultant, AI Research and Health Insights at [Gluroo Imaginations Inc](https://gluroo.com/). Christopher's research focuses on finding ways to utilize a wide variety of AI tools for easing and improving diabetes management. Christopher has Latent Autoimmune Diabetes of Adults (LADA) a subtype of T1D.

#### Walker Payne :syringe: :droplet:

[Walker Payne](https://www.linkedin.com/in/walker-payne/) is a data scientist at [Gluroo](https://www.gluroo.com). He is also a type 1 diabetic, having been diagnosed nearly 15 years ago.

#### Dvir Zagury-Grynbaum

[Dvir Zagury-Grynbaum](https://www.linkedin.com/in/dvirzagury/) is a mathematical physics undergraduate student at the University of Waterloo with research and application experience in causal inference and causal AI. He will bring his expertise to help answer questions standard ML tools have trouble with in finite data scenarios where Randomized Controlled Trials are not always possible, such as diabetes health data scenarios.

### Core Members:

#### Abdullah Shahid :syringe: :droplet:

[Abdullah Shahid](https://www.linkedin.com/in/abdullahshahid247/) is a computer science undergraduate at the University of Waterloo. Diagnosed with Type 1 Diabetes nearly a decade ago, he has developed a diabetic lifestyle management app as a personal project in the past and has interned at companies like Lyft. He aims to leverage his experience to make life easier for diabetics around the world.

#### Andrew Yang

[Andrew Yang](https://www.linkedin.com/in/andrewatyang/) is Big Mac on Discord.

#### TBD [...]

### Stakeholder Members:

Stakeholder members will be PWDs with much to contribute in the form of knowledge and lived experience but may not have the time or ability to contribute to development, coding, or writing.
