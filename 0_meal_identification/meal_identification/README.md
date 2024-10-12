# Meal Identification

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

Developing ai algorithms for automatic meal detection from blood glucose concentration cgm data.

## Project Organization

```
├── LICENSE            <- Open-source license if one is chosen
├── Makefile           <- Makefile with convenience commands like `make data` or `make train`
├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── external       <- Data from third party sources.
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── docs               <- A default mkdocs project; see www.mkdocs.org for details
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
│
├── pyproject.toml     <- Project configuration file with package metadata for 
│                         meal_identification and configuration for tools like black
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── setup.cfg          <- Configuration file for flake8
│
└── meal_identification   <- Source code for use in this project.
    │
    ├── __init__.py             <- Makes meal_identification a Python module
    │
    ├── config.py               <- Store useful variables and configuration
    │
    ├── dataset.py              <- Scripts to download or generate data
    │
    ├── features.py             <- Code to create features for modeling
    │
    ├── modeling                
    │   ├── __init__.py 
    │   ├── predict.py          <- Code to run model inference with trained models          
    │   └── train.py            <- Code to train models
    │
    └── plots.py                <- Code to create visualizations
```

--------

## How to Start Contributing
This will be an iterative development cycle where you develop your time series annotation models in .ipynb. Once your notebook has demonstrated something useful, we will move it to the source code directory so others can reuse it and set it up for large-scale hyperparameter tuning.

Check out this sktime example: [Time Series Segmentation with sktime and ClaSP](https://www.sktime.net/en/stable/examples/annotation/segmentation_with_clasp.html)

skTime already has many time series annotation algorithms available through its API: 
* [sktime time series annotation API](https://www.sktime.net/en/stable/api_reference/annotation.html)

We want to try out every one of these algorithms and evaluate which ones work best with our problem. 
Go ahead and start creating an ipynb following the file naming conventions outlines in the notebooks directory. 
Please try to follow the [PEP8](https://peps.python.org/pep-0008/) Style Guide in your development to facilitate the transfer to source code. 
