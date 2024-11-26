# Detector sktime Implementation Prioritization

## Meta Data
| Algorithm | Literature | Hyperparameters |
| ----------- | ----------- | ----------- |
| Binary Segmentation  |  |
| Fused Lasso |  |
| Opt |  |
| Pelt |  |
| Window |  |

* **Detection Type**: points, segments, both, something else
    * segment = (start time stamp, end time stamp)
    * if segments, can they overlap
    * are labels deterministic, or probabilistic (probability of segment)
* **type of label meaning**: outlier/anomaly, changepoint, mixed/multiple, something else
* **Parametric/Non-parametric**: Is the model a parametric or non-parametric
* **Score**: does the algorithm also return a score, e.g., anomaly score
* **Cost Function**:
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


## Cost Functions
| Cost Function | Algorithm/Model Subtype | Detection Type | Parametric/Non-parametric | Score? | Search Method | Label Annotation Present? | Learning Type | Learning Mode | Univariate | Multivariate | Online/Offline | Problem Type | Time Series scitype |
| ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ---------- |
| $c_{i.i.d.}(y_{a.b})$ | maximum likelihood estimation | change point | parametric |  |  |  |  |  |  |  |  |  |  |  |
| $c_{L_{2}}(y_{a.b})$ | maximum likelihood estimation | change point | parametric |  |  |  |  |  |  |  |  |  |  |  |
| $c_{\Sigma}(y_{a.b})$ | maximum likelihood estimation | change point | parametric |  |  |  |  |  |  |  |  |  |  |  |
| $c_{Poisson}(y_{a.b})$ | maximum likelihood estimation | change point | parametric |  |  |  |  |  |  |  |  |  |  |  |
| $c_{linear}(y_{a.b})$ | piecewise linear regression | change point | parametric |  |  |  |  |  |  |  |  |  |  |  |
| $c_{linear,L_{1}}(y_{a.b})$ | piecewise linear regression | change point | parametric |  |  |  |  |  |  |  |  |  |  |  |
| $c_{AR}(y_{a.b})$ | piecewise linear regression | change point | parametric |  |  |  |  |  |  |  |  |  |  |  |
| $c_{M}(y_{a.b})$| Mahalanobis-type metric | change point | parametric |  |  |  |  |  |  |  |  |  |  |  |
| $c_{\hat{F}}(y_{a.b})$ | non-parametric maximum likelihood estimation | change point | non-parametric |  |  |  |  |  |  |  |  |  |  |  |
| $c_{rank}(y_{a.b})$ | rank-based | change point | non-parametric |  |  |  |  |  |  |  |  |  |  |  |
| $c_{kernel}(y_{a.b})$ | kernel-based | change point | non-parametric |  |  |  |  |  |  |  |  |  |  |  |
| $c_{rbf}(y_{a.b})$ | kernel-based | change point | non-parametric |  |  |  |  |  |  |  |  |  |  |  |
| $c_{\mathcal{H},M}(y_{a.b})$ | kernel-based | change point | non-parametric |  |  |  |  |  |  |  |  |  |  |  |
| |  |  |  |  |  |  |  |  |  |  |  |  |  |


## Metrics
| Metric Type | Description | Math Description | Source |
| - | - | --- | - |
| Annotation error | Difference between the predicted  number of cps and actual cps | $\Delta_{AE}(\mathcal{T}^{*},\hat{\mathcal{T}}):=\|\hat{K} - K^{*}\|$ | [(C. Truong 2020, Sec.3)](https://www.sciencedirect.com/science/article/pii/S0165168419303494)|
| Hausdorff error | The greatest temporal distance between a change point and its prediction | $\Delta_{HA}(\mathcal{T}^{*},\hat{\mathcal{T}}):= \max{\{\max_{\hat{t}\in\hat{\mathcal{T}}} \min_{t^{*}\in\mathcal{T}^{*}} \|\hat{t}-t^{*}\|,\max_{t^{*}\in \mathcal{T}^{*}} \min_{\hat{t}\in\hat{\mathcal{T}}}\|\hat{t}-t^{*}\|\}}$ | [(C. Truong 2020, Sec.3)](https://www.sciencedirect.com/science/article/pii/S0165168419303494) |
| Rand index | The average similarity between the predicted breakpoint set $\hat{\mathcal{T}}$ and the ground truth $\mathcal{T}^{*}$. An agreement is when a pair of indexes are in the same segment. | $\Delta_{RI}(\mathcal{T}^{*}, \hat{\mathcal{T}}):=\frac{\|gr(\hat{\Tau}) \cap gr(\mathcal{T}^{*}) \| + \|ngr(\hat{\Tau}) \cap ngr(\mathcal{T}^{*}) \|}{T(T-1)}$ | [(C. Truong 2020, Sec.3)](https://www.sciencedirect.com/science/article/pii/S0165168419303494) |
| F1-Score | Precision is the proportion of predicted change points that are true change points. Recall is the proportion of true change points that are well predicted.  | $\Delta_{F1}(\mathcal{T}^{*},\hat{\mathcal{T}}):=2\times\frac{PREC(\mathcal{T}^{*},\hat{\mathcal{T}}) \times REC(\mathcal{T}^{*},\hat{\mathcal{T}})}{PREC(\mathcal{T}^{*},\hat{\mathcal{T}}) + REC(\mathcal{T}^{*},\hat{\mathcal{T}})}$ | [(C. Truong 2020, Sec.3)](https://www.sciencedirect.com/science/article/pii/S0165168419303494) |
|  | |  | |



## Implementation Libraries
| Authors | Repo URL | pypi name | Code Status Language | License Type | Maintained | Governance Model |
| ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- |
| C. Truong, L. Oudre, N. Vayatis  | https://centre-borelli.github.io/ruptures-docs/ | [ruptures](https://pypi.org/project/ruptures/)  | python  | [BSD 2-Clause License](https://centre-borelli.github.io/ruptures-docs/#license) | yes |  |
|  |  |  |  |  |  |  |


## Papers to Review Prioritization:
1. [An Evaluation of Change Point Detection Algorithms](https://arxiv.org/pdf/2003.06222)
2. [Selective review of offline change point detection methods](https://doi.org/10.1016/j.sigpro.2019.107299)
3. [Papers with Code - Change Point Detection](https://paperswithcode.com/task/change-point-detection)
4. [A survey of methods for time series change point detection](https://link.springer.com/article/10.1007/s10115-016-0987-z)
5. [Semi-supervised Sequence Classification through Change Point Detection](https://ojs.aaai.org/index.php/AAAI/article/view/16814)
