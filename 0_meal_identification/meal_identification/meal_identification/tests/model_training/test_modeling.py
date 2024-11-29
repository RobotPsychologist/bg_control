import unittest

from meal_identification.modeling.train import ScaledLogitTransformer, train_model_instance, load_data, xy_split, process_labels, load_model, save_model

from meal_identification.config import (
    MODELS_DIR, 
    INTERIM_DATA_DIR
)

class TestTrainingScript(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Fixture for mock paths of data and model."""
        cls.data_path = INTERIM_DATA_DIR / "2024-11-15_500030__i5mins_d4hrs_c5g_l2hrs_n3.csv"
        cls.model_path = MODELS_DIR / "GMMHMM_model"
        cls.sample_data = load_data(cls.data_path)
        cls.sample_model = load_model(cls.model_path)

    def test_load_data(self):
        """Test that data loads correctly from the CSV."""
        sample_data = self.sample_data
        assert sample_data.shape == (sample_data.shape[0], 10)  # Adjust this based on actual data shape
        assert "bgl" in sample_data.columns


    def test_xy_split(self):
        """Test splitting data into features and target."""
        X, Y = xy_split(self.sample_data)
        assert X.shape == (X.shape[0], 1)  # 'bgl' column should be present
        assert Y.shape == (Y.shape[0], 1)  # msg_type should be the target


    def test_process_labels(self):
        """Test the label processing."""
        _, Y = xy_split(self.sample_data)
        Y = process_labels(Y)
        assert set(Y["msg_type"]) == {0, 1}  # Assuming binary classification

    def test_save_model(self):
        """Test saving the model."""
        # Train the model
        gmmhmm_model = train_model_instance(
            model="GMMHMM",
            data_path=self.data_path,
            model_path=self.model_path,
            transformer=ScaledLogitTransformer()
        )
        # Check if the model was saved correctly
        save_model(
            model=gmmhmm_model,
            model_path=str(self.model_path),
        )


    def test_model_training(self):
        """Test the full model training process with actual data."""

        # Perform model training
        train_model_instance(
            model="GMMHMM",
            data_path=self.data_path,
            model_path=self.model_path,
            transformer=ScaledLogitTransformer()
        )

        # Check that the model file exists after training
        assert self.model_path.exists()