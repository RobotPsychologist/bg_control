import pytest
import pandas as pd
from meal_identification.datasets.dataset_cleaner import erase_meal_overlap_fn, keep_top_n_carb_meals
from meal_identification.datasets.PydanticModels import DataFrameValidator

class TestMealOverlap:
    def test_meal_overlap_structure(self, sample_meal_df, meal_length, min_carbs):
        """
        Tests that the output DataFrame maintains valid data types using pydantic
        """
        result_df = erase_meal_overlap_fn(sample_meal_df, meal_length, min_carbs)
        assert DataFrameValidator.validate_meal_df(result_df)
    
    def test_food_g_sum(self, sample_meal_df, meal_length, min_carbs):
        """
        Tests that the food_g sum is the same as the original food_g sum
        (though not comprehensive, attempting to calculate the sum in each window would be circular- we would be
        testing a function while using the same function to test it)
        """
        result_df = erase_meal_overlap_fn(sample_meal_df, meal_length, min_carbs)
        assert result_df['food_g'].sum() == sample_meal_df['food_g'].sum()

    def test_non_meal_entries_unchanged(self, sample_meal_df, meal_length, min_carbs):
        """
        Tests that non-meal entries remain unchanged
        """
        result_df = erase_meal_overlap_fn(sample_meal_df, meal_length, min_carbs)
        assert (result_df[result_df['msg_type'] == ''] == sample_meal_df[sample_meal_df['msg_type'] == '']).all()

    def test_overlapping_meals_combined(self, sample_meal_df, meal_length, min_carbs):
        """
        Tests that overlapping meals are combined
        """
        result_df = erase_meal_overlap_fn(sample_meal_df, meal_length, min_carbs)
        
        # Find any meal that had overlapping meals combined
        announce_meal_mask = result_df['msg_type'] == 'ANNOUNCE_MEAL'
        original_meals = sample_meal_df[sample_meal_df['msg_type'] == 'ANNOUNCE_MEAL']
        combined_meals = result_df[announce_meal_mask]
        
        # At least one meal should have a higher carb value than any original meal
        assert any(combined_meals['food_g'] > original_meals['food_g'].max())

    def test_min_carbs_threshold(self, sample_meal_df, meal_length, min_carbs):
        """
        Tests that meals below the min_carbs threshold are not combined
        """
        result_df = erase_meal_overlap_fn(sample_meal_df, meal_length, min_carbs)
        assert (result_df[result_df['food_g'] < min_carbs]['food_g'] == sample_meal_df[sample_meal_df['food_g'] < min_carbs]['food_g']).all()
        
