from pathlib import Path
import typer
from loguru import logger
from tqdm import tqdm
from sklearn.model_selection import train_test_split
from meal_identification.config import MODELS_DIR, PROCESSED_DATA_DIR

# Model Imports
from sktime.annotation.hmm_learn import GMMHMM 
from sktime.annotation.clasp import ClaSPSegmentation, find_dominant_window_sizes
from sktime.classification.interval_based import TimeSeriesForestClassifier
from pyod.models.knn import KNN
from sktime.annotation.adapters import PyODAnnotator
from sktime.annotation.lof import SubLOF
from hmmlearn import hmm # CategoricalHMM and GaussianHMM uses hmm module
from sktime.annotation.hmm_learn import PoissonHMM 

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

    def train_model(X, Y, validation_split = 0.2, model="model", hyperparameters = []):
        """
        Train a model on the given data.

        Parameters
        ----------
        X : pd.DataFrame
            Features.
        Y : pd.Series
            Labels.
        validation_split : float, optional
            Fraction of the data to use for validation, by default 0.2
        model : str, optional
            Model to train, by default "model"
        hyperparameters : list, optional
            Hyperparameters for the model, by default []

        Returns
        -------
        model
            Trained model. And logs the training process.
        """

        # Split the data into training and validation sets
        X_train, X_val, Y_train, Y_val = train_test_split(X, Y, test_size=validation_split)
        pass

    logger.info("Training some model...")
    for i in tqdm(range(10), total=10):
        if i == 5:
            logger.info("Something happened for iteration 5.")
    logger.success("Modeling training complete.")
    # -----------------------------------------


if __name__ == "__main__":
    app()
