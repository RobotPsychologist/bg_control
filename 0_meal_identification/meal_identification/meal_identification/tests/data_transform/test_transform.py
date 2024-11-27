import pytest
import pandas as pd
import os
import tempfile
import shutil
import unittest
from meal_identification.transformations.pipeline_generator import PipelineGenerator
from meal_identification.transformations.pydantic_test_models import NumericColumns, CategoricalColumns, CosineTransformed
from meal_identification.datasets.pydantic_test_models import DataFrameValidator
from sktime.transformations.series.cos import CosineTransformer

from sktime.transformations.series.impute import Imputer

class TestTransformation(unittest.TestCase):
    def setUp(self):
        """Set up test environment with temporary directory and sample CSV files."""
        self.project_root = os.path.realpath(tempfile.mkdtemp())
        os.makedirs(os.path.join(self.project_root, '.github'))

        # Create interim and processed data directory
        self.interim_data_dir = "0_meal_identification/meal_identification/data/interim"
        self.full_interim_path = os.path.join(self.project_root, self.interim_data_dir)
        os.makedirs(self.full_interim_path)
        
        self.processed_data_dir = "0_meal_identification/meal_identification/data/processed"
        self.full_processed_path = os.path.join(self.project_root, self.processed_data_dir)
        os.makedirs(self.full_processed_path)

        # Make it as a pd frame, then convert it to a csv for readability
        self.sample_interim_data = pd.DataFrame({
            'date': [
                '2024-07-01 00:00:00-04:00',
                '2024-07-01 00:05:00-04:00'
            ],
            'bgl': [115.0, 112.0],
            'msg_type': ['ANNOUCE_MEAL', 'DOSE_INSULIN'],
            'affects_fob': [False, None],
            'affects_iob': [None, True],
            'dose_units': [None, None],
            'food_g': [None, None],
            'food_glycemic_index': [None, None],
            'food_g_keep': [None, None],
            'day_start_shift':['2024-06-30', '2024-06-30']
        })

        # Convert date strings to datetime objects before saving
        self.sample_interim_data['date'] = pd.to_datetime(self.sample_interim_data['date'])

        # Save sample CSV files
        self.filename = 'interim_data.csv'
        self.file_path = os.path.join(self.full_interim_path, self.filename)
        self.sample_interim_data.to_csv(self.file_path, index=False)
        self.original_dir = os.getcwd()
        os.chdir(self.project_root)


    def tearDown(self):
        """Clean up temporary files and directories."""
        os.chdir(self.original_dir)
        shutil.rmtree(self.project_root)

    def test_load_numerical_data(self):
        """
        Tests that the numerical columns of loaded data maintains valid data types using pydantic
        """
        interim_file = self.filename
        gen = PipelineGenerator()
        gen.load_data([interim_file])
        result_df = gen.data_num[interim_file]
        print(result_df.columns)
        assert DataFrameValidator(NumericColumns, index_field='bgl').validate_df(result_df)
    
    def test_load_categorical_data(self):
        """
        Tests that the categorical columns of loaded data maintains valid data types using pydantic
        """
        interim_file = self.filename
        gen = PipelineGenerator()
        gen.load_data([interim_file])
        result_df = gen.data_cat[interim_file]
        # dfs are not indexed with date col
        assert DataFrameValidator(CategoricalColumns, index_field='date').validate_df(result_df, True)


    def test_transformed(self):
        """
        Tests if transformed data has numerical values between -1 and 1
        """
        interim_file = self.filename
        gen = PipelineGenerator()
        gen.load_data([interim_file])
        gen.generate_pipeline([
            CosineTransformer(),
            Imputer(method = "constant", value = 0)
        ])
        gen.fit_transform()
        result_df = gen.save_output()[interim_file]
        assert DataFrameValidator(CosineTransformed, index_field='date').validate_df(result_df, True)
