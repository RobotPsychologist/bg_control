from meal_identification.datasets.dataset_operations import load_data
import unittest
import os
import tempfile
import shutil
import pandas as pd
from meal_identification.datasets.PydanticModels import DataFrameValidator, RawMealRecord

class TestLoadData(unittest.TestCase):
    def setUp(self):
        """Set up test environment with temporary directory and sample CSV files."""
        self.project_root = os.path.realpath(tempfile.mkdtemp())
        os.makedirs(os.path.join(self.project_root, '.github'))

        # Create raw data directory
        self.raw_data_dir = "data/raw"
        self.full_raw_path = os.path.join(self.project_root, self.raw_data_dir)
        os.makedirs(self.full_raw_path)

        # Make it as a pd frame, then convert it to a csv for readability
        self.sample_data = pd.DataFrame({
            'date': [
                '2024-07-01 00:02:39-05:00',
                '2024-07-01 00:07:39-05:00'
            ],
            'sender_id': [None, None],
            'bgl': [98.0, 100.0],
            'bgl_date_millis': [None, None],
            'text': [None, None],
            'template': [None, None],
            'msg_type': ['ANNOUNCE_MEAL', 'DOSE_INSULIN'],
            'affects_fob': [None, None],
            'affects_iob': [None, None],
            'dose_units': [None, None],
            'food_g': [None, None],
            'food_glycemic_index': [None, None],
            'dose_automatic': [None, None],
            'fp_bgl': [None, None],
            'message_basal_change': [None, None],
            '__typename': ['Reading', 'Reading'],
            'trend': ['FORTYFIVE_UP', 'FORTYFIVE_UP']
        })

        # Convert date strings to datetime objects before saving
        self.sample_data['date'] = pd.to_datetime(self.sample_data['date'])

        # Save sample CSV files
        self.filename = 'glucose_readings.csv'
        self.file_path = os.path.join(self.full_raw_path, self.filename)
        self.sample_data.to_csv(self.file_path, index=False)
        self.original_dir = os.getcwd()
        os.chdir(self.project_root)

        # What we wanna keep
        self.default_keep_cols = ['date', 'bgl', 'msg_type']

    def tearDown(self):
        """Clean up temporary files and directories."""
        os.chdir(self.original_dir)
        shutil.rmtree(self.project_root)

    def test_validate_structure(self):
        """
        Test that the output DataFrame maintains valid structure via pydantic
        """
        result_df = load_data("data/raw", self.default_keep_cols)
        assert DataFrameValidator(RawMealRecord, index_field="date").validate_df(result_df[self.filename], is_raw=True)


    def test_successful_load(self):
        """Test successful loading of CSV files with specified columns."""
        keep_cols = ['date', 'bgl']
        result = load_data(self.raw_data_dir, keep_cols)

        self.assertEqual(len(result), 1)
        self.assertIn(self.filename, list(result.keys())[0])

        # Check if only specified columns are kept
        for df in result.values():
            self.assertEqual(set(df.columns), set(keep_cols))

    def test_nonexistent_directory(self):
        """Test handling of non-existent directory."""
        with self.assertRaises(FileNotFoundError):
            load_data('nonexistent_dir', ['date', 'value'])

    def test_invalid_columns(self):
        """Test handling of invalid column names."""
        keep_cols = ['date', 'nonexistent_column']
        result = load_data(self.raw_data_dir, keep_cols)
        self.assertEqual(len(result), 0)
