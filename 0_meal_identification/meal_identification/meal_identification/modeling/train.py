from pathlib import Path
import typer
from loguru import logger
from tqdm import tqdm
import pandas as pd
import os
from sklearn.model_selection import train_test_split
from meal_identification.config import MODELS_DIR, PROCESSED_DATA_DIR
from sktime.performance_metrics.forecasting import count_error, hausdorff_error, prediction_ratio

# Model Imports
from sktime.annotation.hmm_learn import GMMHMM 
from sktime.annotation.clasp import ClaSPSegmentation, find_dominant_window_sizes
from sktime.classification.interval_based import TimeSeriesForestClassifier
from pyod.models.knn import KNN
from sktime.annotation.adapters import PyODAnnotator
from sktime.annotation.lof import SubLOF
from hmmlearn import hmm  # CategoricalHMM and GaussianHMM use hmm module
from sktime.annotation.hmm_learn import PoissonHMM 
from sktime.annotation.hmm_learn import GaussianHMM
import joblib  # Added import for joblib

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
        joblib.dump(model, model_path)
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
        model = joblib.load(model_path)
        logger.info(f"Model loaded from {model_path}")
        return model
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        return None

@app.command()
def main(
    # ---- REPLACE DEFAULT PATHS AS APPROPRIATE ----
    features_path: Path = PROCESSED_DATA_DIR / "features.csv",
    labels_path: Path = PROCESSED_DATA_DIR / "labels.csv",
    model_path: Path = MODELS_DIR / "model.pkl",
    # -----------------------------------------
):
    def transform_data(data, transformer):
        """
        Transform the data using the given transformer.

        Parameters
        ----------
        data : pd.Series
            Data to transform.
        transformer : sktime transformer
            Transformer to use.

        Returns
        -------
        pd.Series
            Transformed data.
        """
        transformed_data = transformer.fit_transform(data)
        
        # Save the transformed data to the specified directory
        output_path = Path("0_meal_identification/meal_identification/data/processed/transformed_data.csv")
        transformed_data.to_csv(output_path, index=False)
        
        return transformed_data
    
    def load_data(csv_path: Path):
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

    
    def xy_split(data):
        """
        Split the data into features and labels.

        Parameters
        ----------
        data : pd.DataFrame
            Data to split.

        Returns
        -------
        pd.Series
            Features.
        pd.Series
            Labels.
        """
        X = data(columns=["bgl"])
        Y = data["msg_type"]
        
        return X, Y

    def train_model_instance(data_path, model="model", supervised=False, 
                             validation_split=0.2, n_iter=100, 
                             n_components=3, n_mix=3, covariance_type='full', 
                             verbose=True, period_length=10, n_cps=2, 
                             n_neighbors=36, window_size=288, init_params="s", 
                             random_state=None, transformer=None, model_path=None):
        """
        Train a model on the given data.

        Parameters
        ----------
        X : csv file path
            BGL data.
        Y : csv file path
            Labels.
        transformer : callable, optional
            A function or transformer that preprocesses the data.
        supervised : bool, optional
            Indicates whether the model is supervised.
        validation_split : float, optional
            Fraction of the data to use for validation, by default 0.2
        model : str, optional
            Model to train, by default "model"

        hyperparameters :
            Hyperparameters for the model
            GMMHMM: n_components, n_mix, covariance_type
            ClaSPSegmentation: period_length, n_cps
            SubLOF: n_neighbors, window_size
            PoissonHMM: n_components, n_iter, init_params, random_state, verbose
            GaussianHMM: n_components, covariance_type, n_iter, init_params, random_state, verbose

        Returns
        -------
        model
            Trained model

        Notes
        -----
        Training logs are saved to the 'models/training_logs' directory.
        """

        log_dir = 'models/training_logs'
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, f'{model}_training.log')

        logger.add(log_file)

        # Load the data
        data = load_data(data_path)
        X, Y = xy_split(data)
        # Apply the transformer to the data
        X = transform_data(data = X, transformer=transformer)
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

        if model_path:  # Add this condition to save the model after training
            save_model(model, model_path)

        return model

    logger.info("Training some model...")
    for i in tqdm(range(10), total=10):
        if i == 5:
            logger.info("Something happened for iteration 5.")
    logger.success("Modeling training complete.")
    # -----------------------------------------

if __name__ == "__main__":
    app()
