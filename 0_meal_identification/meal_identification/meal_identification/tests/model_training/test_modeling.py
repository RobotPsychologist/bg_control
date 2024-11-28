
"""
python -m unittest meal_identification/tests/model_training/test_modeling.py
"""
import unittest
from unittest.mock import patch
import pandas as pd
from pathlib import Path
from meal_identification.modeling.train import ScaledLogitTransformer, GMMHMM, train_model_instance, load_data, xy_split, process_labels

def mock_paths():
    """Fixture for mock paths of data and model."""
    data_path = Path("0_meal_identification/meal_identification/data/interim/2024-11-15_500030__i5mins_d4hrs_c5g_l2hrs_n3.csv")
    model_path = Path("0_meal_identification/meal_identification/models/model.pkl")
    return data_path, model_path


def sample_data(mock_paths):
    """Load sample data from CSV for testing."""
    data_path, _ = mock_paths
    return load_data(data_path)


def test_load_data(sample_data):
    """Test that data loads correctly from the CSV."""
    assert sample_data.shape == (len(sample_data), 16)  # Adjust this based on actual data shape
    assert "bgl" in sample_data.columns


def test_xy_split(sample_data):
    """Test splitting data into features and target."""
    X, Y = xy_split(sample_data)
    assert X.shape == (len(sample_data), 1)  # 'bgl' column should be present
    assert Y.shape == (len(sample_data), 1)  # msg_type should be the target


def test_process_labels(sample_data):
    """Test the label processing."""
    _, Y = xy_split(sample_data)
    Y = process_labels(Y)
    assert set(Y["msg_type"]) == {0, 1}  # Assuming binary classification


@patch("meal_identification.model_training.train.mlflow_sktime.save_model")
def test_save_model(mock_save_model, mock_paths):
    """Test saving the model."""
    _, model_path = mock_paths
    # Train the model
    train_model_instance(
        model="GMMHMM",
        data_path=mock_paths[0],
        model_path=model_path,
        transformer=ScaledLogitTransformer()
    )
    # Check if the model was saved correctly
    mock_save_model.assert_called_once_with(
        sktime_model=GMMHMM(),
        path=str(model_path),
        serialization_format="pickle"
    )


def test_model_training(mock_paths):
    """Test the full model training process with actual data."""
    data_path, model_path = mock_paths

    # Perform model training
    train_model_instance(
        model="GMMHMM",
        data_path=data_path,
        model_path=model_path,
        transformer=ScaledLogitTransformer()
    )

    # Check that the model file exists after training
    assert model_path.exists()

if __name__ == "__main__":
    unittest.main()
