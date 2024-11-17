import pytest
import pandas as pd
from meal_identification.datasets.dataset_cleaner import erase_meal_overlap_fn, keep_top_n_carb_meals
from meal_identification.datasets.pydantic_test_models import DataFrameValidator, MealRecord

class TestMealOverlap:
    def test_meal_overlap_structure(self, sample_meal_df, meal_length, min_carbs):
        """
        Tests that the output DataFrame maintains valid data types using pydantic
        """
        result_df = erase_meal_overlap_fn(sample_meal_df, meal_length, min_carbs)
        assert DataFrameValidator(MealRecord).validate_df(result_df)
    
    def test_food_g_sum(self, sample_meal_df, meal_length, min_carbs):
        """
        Tests that the food_g sum is the same as the original food_g sum
        (though not comprehensive, attempting to calculate the sum in each window would be circular- we would be
        testing a function while using the same function to test it)
        """
        result_df = erase_meal_overlap_fn(sample_meal_df, meal_length, min_carbs)
        assert result_df['food_g'].sum() == sample_meal_df['food_g'].sum()


    def test_overlapping_meals_combined(self, sample_meal_df, meal_length, min_carbs):
        """
        Tests that overlapping meals are combined correctly by checking:
        1. All food_g values after an ANNOUNCE_MEAL within meal_length window are 0
        2. The ANNOUNCE_MEAL entry contains the sum of all food_g in its window
        """
        result_df = erase_meal_overlap_fn(sample_meal_df, meal_length, min_carbs)
        
        # Get all ANNOUNCE_MEAL entries
        announce_meal_indices = result_df[result_df['msg_type'] == 'ANNOUNCE_MEAL'].index
        
        for idx in announce_meal_indices:
            window_end = idx + meal_length
            window_entries = result_df.loc[idx + pd.Timedelta(seconds=1):window_end]
            
            # Check that all food_g values in window after ANNOUNCE_MEAL are 0
            assert (window_entries['food_g'] == 0).all(), f"Found non-zero food_g values after ANNOUNCE_MEAL at {idx}"
            
            # Check that the ANNOUNCE_MEAL entry contains the sum from original data
            original_window = sample_meal_df.loc[idx:window_end]
            expected_sum = original_window['food_g'].sum()
            assert result_df.at[idx, 'food_g'] == expected_sum, \
                f"ANNOUNCE_MEAL at {idx} does not contain correct sum of food_g values"

    def test_min_carbs_threshold(self, sample_meal_df, meal_length, min_carbs):
        """
        Tests that all ANNOUNCE_MEAL entries have at least min_carbs food_g
        """
        result_df = erase_meal_overlap_fn(sample_meal_df, meal_length, min_carbs)
        announce_meals = result_df[result_df['msg_type'] == 'ANNOUNCE_MEAL']
        assert (announce_meals['food_g'] >= min_carbs).all(), "Found ANNOUNCE_MEAL entries with food_g below min_carbs threshold"

