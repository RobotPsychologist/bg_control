# Detector sktime Implementation Prioritization

## Meta Data
| Algorithm | Literature | Hyperparameters |
| ----------- | ----------- | ----------- |
|  |  |
|  |  |


## Abstract Typing
| Algorithm | Detection Type | Score? | Label Annotation Present? | Learning Type | Learning Mode | Univariate | Multivariate | Online/Offline | Time Series scitype |
| ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- |
|  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |



* **Detection Type**: points, segments, both, something else
    * segment = (start time stamp, end time stamp)
    * if segments, can they overlap
    * are labels deterministic, or probabilistic (probability of segment)
* **type of label meaning**: outlier/anomaly, changepoint, mixed/multiple, something else
* **Score**: does the algorithm also return a score, e.g., anomaly score
* **label annotation present?**: If yes: categorical, numerical
* **learning type**: supervised, unsupervised, semi-supervised
* **learning mode**: stream, batch, both
* **Univariate/Multivariate**: univariate only or multivariate capability
* **Online/Offline**:
  * **online** aim to detect changes as they occur in real-time settings.
    * often refers to *event* or *anomaly detection*
  * **offline** retrospectively detect changes when all sames are collected.
    * Also called *signal segmentation*
    * Also referred to as *retrospective* or *a posteriori*
* **time series scitype**: single time series, panel/collection, hierarchical, multiple of these, something else.

## Metrics



## Implementation Libraries
| Authors | Repo URL | pypi name | Code Status Language | License Type | Maintenance Status | Governance Model |
| ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- |
| C. Truong, L. Oudre, N. Vayatis  | https://centre-borelli.github.io/ruptures-docs/ |  |  | BSD 2-Clause License |  |  |
|  |  |  |  |  |  |  |
