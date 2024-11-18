# Detector sktime Implementation Prioritization

## Meta Data
| Algorithm | Literature | Hyperparameters |
| ----------- | ----------- | ----------- |
|  |  |
|  |  |


## Abstract Typing
| Algorithm | Detection Type | Score? | Cost Function | Search Method | Label Annotation Present? | Learning Type | Learning Mode | Univariate | Multivariate | Online/Offline | Problem Type | Time Series scitype |
| ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- |
|  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |



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
* **Constraint Type**: which category of change point detection does the model fall under:
  * **Problem 1**: known number of changes
  * **Problem 2**: unknown number of changes

## Metrics
| Metric Type | Description | Math Description |
| - | - | --- |
| Annotation error | Difference between the predicted  number of cps and actual cps | $\Delta_{AE}(\mathcal{T}^{*},\hat{\mathcal{T}}):=\|\hat{K} - K^{*}\|$ |
| Hausdorff error | the greatest temporal distance between a chance point and its prediction | $\Delta_{HA}(\mathcal{T}^{*},\hat{\mathcal{T}}):= \max{\{\max_{\hat{t}\in\hat{\mathcal{T}}} \min_{t^{*}\in\mathcal{T}}^{*} \|\hat{t}-t^{*}\|,\max_{t^{*}\in \mathcal{T}^{*}} \min_{\hat{t}\in\hat{\mathcal{T}}}\|\hat{t}-t^{*}\|\}}$ |
| Rand index | |  |
| F1-Score | |  |
|  | |  |



## Implementation Libraries
| Authors | Repo URL | pypi name | Code Status Language | License Type | Maintained | Governance Model |
| ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- |
| C. Truong, L. Oudre, N. Vayatis  | https://centre-borelli.github.io/ruptures-docs/ | [ruptures](https://pypi.org/project/ruptures/)  | python  | [BSD 2-Clause License](https://centre-borelli.github.io/ruptures-docs/#license) | yes |  |
|  |  |  |  |  |  |  |
