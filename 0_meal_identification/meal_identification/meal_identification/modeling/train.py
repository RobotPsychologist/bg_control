from pathlib import Path
import typer
from loguru import logger
from tqdm import tqdm
import pandas as pd
import os
import sktime as sktime
from sklearn.model_selection import train_test_split
from sktime.utils import mlflow_sktime  
from sktime.performance_metrics.annotation.metrics import count_error
from sktime.performance_metrics.annotation.metrics import hausdorff_error
from sktime.performance_metrics.annotation.metrics import prediction_ratio

# Model Imports
from sktime.annotation.hmm_learn import GMMHMM 
from sktime.annotation.clasp import ClaSPSegmentation
from sktime.annotation.lof import SubLOF
from sktime.annotation.hmm_learn import PoissonHMM 
from sktime.annotation.hmm_learn import GaussianHMM 
from sktime.annotation.igts import InformationGainSegmentation 
from sktime.annotation.stray import STRAY
from sktime.annotation.clust import ClusterSegmenter # needed changing in documentation
from sktime.annotation.eagglo import EAgglo
from sktime.annotation.ggs import GreedyGaussianSegmentation
from sktime.annotation.hmm import HMM

# Transformer Imports
from sktime.transformations.series.scaledlogit import ScaledLogitTransformer

# Paths
from meal_identification.config import (
    MODELS_DIR, 
    PROCESSED_DATA_DIR,
    INTERIM_DATA_DIR
)

app = typer.Typer()

# Function to save a model
def save_model(model, model_path: Path):
    """
    Save the trained model to the specified file path.

    Parameters
    ----------
    model : object
        The model to save.
    model_path : Path
        The path where the model will be saved.
    """
    try:
        mlflow_sktime.save_model(
            sktime_model = model,
            path = str(model_path),
            serialization_format='pickle'
            )
        logger.info(f"Model saved to {model_path}")
    except Exception as e:
        logger.error(f"Error saving model: {e}")

# Function to load a model
def load_model(model_path: Path):
    """
    Load a model from the specified file path.

    Parameters
    ----------
    model_path : Path
        The path from which the model will be loaded.

    Returns
    -------
    model : object
        The loaded model.
    """
    try:
        model = mlflow_sktime.load_model(model_uri = str(model_path))
        logger.info(f"Model loaded from {model_path}")
        return model
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        return None

def transform_data(data, transformer):
    """
    Transform the data using the given transformer.

    Parameters
    ----------
    data : pd.DataFrame
        Data to transform.
    transformer : sktime transformer
        Transformer to use.

    Returns
    -------
    pd.DataFrame
        Transformed data.
    """
                
    data['bgl'] = data['bgl'].fillna(method='ffill')

    transformed_data = transformer.fit_transform(X = data)
    
    return transformed_data

def load_data(csv_path: Path) -> pd.DataFrame:
    """
    Load data from a CSV file into a DataFrame.

    Parameters
    ----------
    csv_path : Path
        The path to the CSV file.

    Returns
    -------
    pd.DataFrame
        The loaded DataFrame.
    """
    try:
        data = pd.read_csv(csv_path)
        logger.info(f"Data loaded from {csv_path}")
        return data
    except Exception as e:
        logger.error(f"Error loading data from {csv_path}: {e}")
        return None


def xy_split(data: pd.DataFrame ):
    """
    Split the data into features and labels.

    Parameters
    ----------
    data : pd.DataFrame
        Data to split.

    Returns
    -------
    pd.DataFrame
        Features.
    pd.DataFrame
        Labels.
    """
    X = data[["bgl"]]
    Y = data[["msg_type"]]
    
    return X, Y

def process_labels(Y: pd.DataFrame) -> pd.DataFrame:
    """
    Process labels with None = 0, ANNOUNCE_MEAL = 1

    Parameters
    ----------
    Y : pd.DataFrame
        Labels to process

    Returns
    -------
    pd.DataFrame
        Processed labels
    """

    Y["msg_type"] = [
        1 if i == 'ANNOUNCE_MEAL' else 0 for i in Y["msg_type"]
    ]

    return Y


def train_model_instance(data_path: Path, model_path: Path, model="GMMHMM", supervised=False, 
                            validation_split=0.2, n_iter=100, 
                            n_components=2, n_mix=3, covariance_type='full', 
                            verbose=True, period_length=10, n_cps=2, 
                            n_neighbors=36, window_size=288, init_params="s",
                            k_max = 3, step = 5, alpha=0.01, k=15, knn_algorithm='ball_tree', 
                            outlier_tail='both', clusterer = None,
                            member=None, penalty=None, max_shuffles = 250,
                            lamb = 1.0, emission_funcs = None, transition_prob_mat = None,
                            initial_probs = None,
                            random_state=None, transformer=None):
    """
    Train a model on the given data.

    Parameters
    ----------
    data_path : Path
        Path to the data CSV file.
    model_path : Path
        Path to save the trained model.
    model : str, optional
        Model to train, by default "GMMHMM".
    supervised : bool, optional
        Indicates whether the model is supervised.
    validation_split : float, optional
        Fraction of the data to use for validation, by default 0.2.
    n_iter : int, optional
        Number of iterations for models that require it, by default 100.
    n_components : int, optional
        Number of components for applicable models, by default 2.
    n_mix : int, optional
        Number of mixtures for applicable models, by default 3.
    covariance_type : str, optional
        Type of covariance for applicable models, by default 'full'.
    verbose : bool, optional
        Verbosity flag, by default True.
    period_length : int, optional
        Period length for segmentation models, by default 10.
    n_cps : int, optional
        Number of change points for segmentation models, by default 2.
    n_neighbors : int, optional
        Number of neighbors for outlier detection models, by default 36.
    window_size : int, optional
        Window size for outlier detection models, by default 288.
    init_params : str, optional
        Initialization parameters for HMM models, by default "s".
    k_max : int, optional
        Maximum number of splits for segmentation models, by default 3.
    step : int, optional
        Step size for segmentation models, by default 5.
    alpha : float, optional
        Alpha value for outlier detection models, by default 0.01.
    k : int, optional
        Number of neighbors for STRAY model, by default 15.
    knn_algorithm : str, optional
        KNN algorithm for STRAY model, by default 'ball_tree'.
    outlier_tail : str, optional
        Tail type for STRAY model, by default 'both'.
    clusterer : object, optional
        Clusterer for ClusterSegmenter model, by default None.
    member : object, optional
        Member function for EAgglo model, by default None.
    penalty : object, optional
        Penalty function for EAgglo model, by default None.
    max_shuffles : int, optional
        Maximum shuffles for GreedyGaussianSegmentation model, by default 250.
    lamb : float, optional
        Lambda value for GreedyGaussianSegmentation model, by default 1.0.
    emission_funcs : list or None, optional
        Emission functions for HMM model, by default None.
    transition_prob_mat : array-like or None, optional
        Transition probability matrix for HMM model, by default None.
    initial_probs : array-like or None, optional
        Initial probabilities for HMM model, by default None.
    random_state : int or None, optional
        Random state for reproducibility, by default None.
    transformer : sktime transformer or None, optional
        A transformer that preprocesses the data, by default None.

    hyperparameters :
        Hyperparameters for each model type:
        - GMMHMM: n_components, n_mix, covariance_type, n_iter, init_params, random_state, verbose
        - ClaSPSegmentation: period_length, n_cps
        - SubLOF: n_neighbors, window_size
        - PoissonHMM: n_components, n_iter, init_params, random_state, verbose
        - GaussianHMM: n_components, covariance_type, n_iter, init_params, random_state, verbose
        - InformationGainSegmentation: k_max, step
        - STRAY: alpha, k, knn_algorithm, outlier_tail
        - ClusterSegmenter: clusterer
        - EAgglo: member, alpha, penalty
        - GreedyGaussianSegmentation: k_max, lamb, max_shuffles, random_state, verbose
        - HMM: emission_funcs, transition_prob_mat, initial_probs

    Returns
    -------
    model
        Trained model.

    Notes
    -----
    Training logs are saved to the 'models/training_logs' directory.
    """

    log_dir = MODELS_DIR / 'training_logs'
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f'{model}_training.log')

    logger.remove()
    logger.add(log_file)

    # Load the data
    data = load_data(data_path)
    if data is None:
        logger.error("Data loading failed. Exiting training.")
        return None
    X, Y = xy_split(data)
    # Apply the transformer to the data
    X = transform_data(data = X, transformer=transformer)
    # Process labels:
    Y = process_labels(Y = Y)
    # Split the data into training and validation sets
    X_train, X_val, Y_train, Y_val = train_test_split(X, Y, test_size=validation_split, shuffle=False)

    if model == "GMMHMM":
        model = GMMHMM(n_components=n_components, 
                        n_mix = n_mix, 
                        covariance_type=covariance_type, 
                        n_iter=n_iter, 
                        init_params=init_params,
                        random_state=random_state,
                        verbose=verbose)
    elif model == "ClaSPSegmentation":
        model = ClaSPSegmentation(period_length=period_length, 
                                    n_cps=n_cps)
    elif model == "SubLOF":
        model = SubLOF(n_neighbors=n_neighbors, window_size=window_size)
    elif model == "PoissonHMM":
        model = PoissonHMM(n_components=n_components,   
                            n_iter=n_iter,
                            init_params=init_params,
                            random_state=random_state,
                            verbose=verbose)
    elif model == "GaussianHMM":
        model = GaussianHMM(n_components=n_components, 
                            covariance_type=covariance_type,
                            n_iter=n_iter,
                            init_params=init_params,
                            random_state=random_state,
                            verbose=verbose)
    elif model == "InformationGainSegmentation":
        model = InformationGainSegmentation(k_max = k_max, step = step)
    elif model == "STRAY":
        model = STRAY(
            alpha=alpha,
            k=k,
            knn_algorithm=knn_algorithm,
            outlier_tail=outlier_tail
        )
    elif model == "ClusterSegmenter":
        model = ClusterSegmenter(clusterer=clusterer)
    elif model == "EAgglo":
        model = EAgglo(member=member, alpha=alpha, penalty=penalty)
    elif model == "GreedyGaussianSegmentation":
        model = GreedyGaussianSegmentation(
            k_max= k_max, 
            lamb= lamb, 
            max_shuffles = max_shuffles, 
            random_state = random_state,
            verbose=verbose
        )
    elif model == "HMM":
        model = HMM(emission_funcs = emission_funcs, 
                    transition_prob_mat = transition_prob_mat, 
                    initial_probs = initial_probs
        )
    else:
        logger.error(f"Unknown model type: {model}")
        return None

    logger.info(f"Training {'supervised' if supervised else 'unsupervised'} model: {model}...")
    try:
        model.fit(X_train, Y_train) if supervised else model.fit(X_train)
    except Exception as e:
        logger.error(f"Error during model fitting: {e}")
        return None
    logger.info("Model training complete.")

    hidden_states_train = model.predict(X_train)
    hidden_states_test = model.predict(X_val)

    train_count_error = count_error(Y_train, hidden_states_train)
    train_hausdorff_error = hausdorff_error(Y_train, hidden_states_train)
    train_prediction_ratio = prediction_ratio(Y_train, hidden_states_train)

    test_count_error = count_error(Y_val, hidden_states_test)
    test_hausdorff_error = hausdorff_error(Y_val, hidden_states_test)
    test_prediction_ratio = prediction_ratio(Y_val, hidden_states_test)

    logger.info(f"count error for training data: {train_count_error}")
    logger.info(f"hausdorff error for training data: {train_hausdorff_error}")
    logger.info(f"prediction ratio for training data: {train_prediction_ratio}")

    logger.info(f"count error for test data: {test_count_error}")
    logger.info(f"hausdorff error for test data: {test_hausdorff_error}")
    logger.info(f"prediction ratio for test data: {test_prediction_ratio}")

    try:
        save_model(model, model_path=model_path)
        logger.info("Model saved to 0_meal_identification/meal_identification/models")
    except Exception as e:
        logger.error(f"Error saving model: {e}")

    return model

@app.command()
def main(       
    # ---- REPLACE DEFAULT PATHS AS APPROPRIATE ----
    features_path: Path = PROCESSED_DATA_DIR / "features.csv",
    labels_path: Path = PROCESSED_DATA_DIR / "labels.csv",
    model_path: Path = MODELS_DIR / "model.pkl",
    # -----------------------------------------
):
    # -----------------------------------------
    # Sample training:
    logger.info("Training some model... test")

    data_filename = "2024-11-15_500030__i5mins_d4hrs_c5g_l2hrs_n3.csv"
    data_path = INTERIM_DATA_DIR / data_filename
    current_model_path = MODELS_DIR / "PoissonHMM_model"

    train_model_instance(
        model = "PoissonHMM", 
        data_path=data_path,    
        model_path=current_model_path,  
        transformer=ScaledLogitTransformer())
    logger.success("Modeling training complete.")

    current_model_path = MODELS_DIR / "GaussianHMM_model"

    train_model_instance(
        model = "GaussianHMM", 
        data_path=data_path,    
        model_path=current_model_path,  
        transformer=ScaledLogitTransformer())
    logger.success("Modeling training complete.")

    current_model_path = MODELS_DIR / "GreedyGaussianSegmentation"

    train_model_instance(
        model = "GreedyGaussianSegmentation", 
        data_path=data_path,    
        model_path=current_model_path,  
        transformer=ScaledLogitTransformer())
    logger.success("Modeling training complete.")

if __name__ == "__main__":
    app()
