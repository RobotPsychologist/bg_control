from pathlib import Path
import typer
from loguru import logger
from tqdm import tqdm
import pandas as pd
import os
from sklearn.model_selection import train_test_split
from meal_identification.config import MODELS_DIR, PROCESSED_DATA_DIR
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, mean_absolute_percentage_error
from sktime.performance_metrics.forecasting import count_error, hausdorff_error, prediction_ratio


# Model Imports
from sktime.annotation.hmm_learn import GMMHMM 
from sktime.annotation.clasp import ClaSPSegmentation, find_dominant_window_sizes
from sktime.classification.interval_based import TimeSeriesForestClassifier
from pyod.models.knn import KNN
from sktime.annotation.adapters import PyODAnnotator
from sktime.annotation.lof import SubLOF
from hmmlearn import hmm # CategoricalHMM and GaussianHMM uses hmm module
from sktime.annotation.hmm_learn import PoissonHMM 
from sktime.annotation.hmm_learn import GaussianHMM 

app = typer.Typer()


@app.command()
def main(
    # ---- REPLACE DEFAULT PATHS AS APPROPRIATE ----
    features_path: Path = PROCESSED_DATA_DIR / "features.csv",
    labels_path: Path = PROCESSED_DATA_DIR / "labels.csv",
    model_path: Path = MODELS_DIR / "model.pkl",
    # -----------------------------------------
):
    # ---- REPLACE THIS WITH YOUR OWN CODE ----

    def train_model_instance(X, Y, transformer = None, model="model", supervised=False, 
                             validation_split = 0.2, n_iter = 100, 
                             n_components = 3, n_mix = 3, covariance_type = 'full', 
                             verbose = True,
                             period_length = 10, n_cps = 2, n_neighbors = 36,
                             window_size = 288, init_params="s", random_state=None):
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
        X = pd.read_csv(X)
        Y = pd.read_csv(Y)
        # Apply the transformer to the data
        X = transformer.fit_transform(X)
        Y = transformer.transform(Y)
        # Split the data into training and validation sets
        X_train, X_val, Y_train, Y_val = train_test_split(X, Y, test_size=validation_split, shuffle=False)

        if model == "GMMHMM":

            # Implement starprob, covars_prior, means_prior

            model = GMMHMM(n_components=n_components, 
                         n_mix = n_mix, 
                         covariance_type=covariance_type, 
                         n_iter=n_iter, 
                         init_params=init_params,
                         random_state=random_state,
                         verbose=verbose)

            # Use metrics made by sktime team when they come out

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
        logger.info("Modeling training complete.")

        hidden_states_train = model.predict(X_train)
        hidden_states_test = model.predict(X_val)

        train_mae = mean_absolute_error(hidden_states_train, Y_train)
        train_mse = root_mean_squared_error(hidden_states_train, Y_train)
        train_rmse = root_mean_squared_error(hidden_states_train, Y_train, squared=False)  # squared=False returns RMSE
        train_mape = mean_absolute_percentage_error(hidden_states_train, Y_train)

        test_mae = mean_absolute_error(hidden_states_test, Y_val)
        test_mse = root_mean_squared_error(hidden_states_test, Y_val)
        test_rmse = root_mean_squared_error(hidden_states_test, Y_val, squared=False)  # squared=False returns RMSE
        test_mape = mean_absolute_percentage_error(hidden_states_test, Y_val)

        logger.info(f"MAE for training data: {train_mae}")
        logger.info(f"MSE for training data: {train_mse}")
        logger.info(f"RMSE for training data: {train_rmse}")
        logger.info(f"MAPE for training data: {train_mape}")

        logger.info(f"MAE for test data: {test_mae}")
        logger.info(f"MSE for test data: {test_mse}")
        logger.info(f"RMSE for test data: {test_rmse}")
        logger.info(f"MAPE for test data: {test_mape}")


        return model


    logger.info("Training some model...")
    for i in tqdm(range(10), total=10):
        if i == 5:
            logger.info("Something happened for iteration 5.")
    logger.success("Modeling training complete.")
    # -----------------------------------------


if __name__ == "__main__":
    app()