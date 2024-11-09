import pytest
import pandas as pd
from meal_identification.datasets.dataset_cleaner import *
from meal_identification.datasets.PydanticModels import *

def test_erase_meal_overlap_validation(sample_meal_df, meal_length, min_carbs):
    """Test erase_meal_overlap_fn with validation"""
    # Process the data
    result_df = erase_meal_overlap_fn(sample_meal_df, meal_length, min_carbs)
    
    # Validate the output
    assert DataFrameValidator.validate_meal_df(result_df)
    
    # Additional checks
    assert all(result_df['food_g'] >= 0)
    assert all(result_df['msg_type'].isin(['ANNOUNCE_MEAL', '', '0']))

def test_keep_top_n_carb_meals_validation(sample_meal_df):
    """Test keep_top_n_carb_meals with validation"""
    n_top_carb_meals = 2
    
    # Process the data
    result_df = keep_top_n_carb_meals(sample_meal_df, n_top_carb_meals)
    
    # Validate the output
    assert DataFrameValidator.validate_meal_df(result_df)
    
    # Check number of meals per day
    for day in result_df['day_start_shift'].unique():
        day_meals = result_df[
            (result_df['day_start_shift'] == day) & 
            (result_df['msg_type'] == 'ANNOUNCE_MEAL')
        ]
        assert len(day_meals) <= n_top_carb_meals

def test_edge_cases(sample_meal_df, meal_length, min_carbs):
    """Test edge cases for both functions"""
    # Empty DataFrame
    empty_df = pd.DataFrame(columns=sample_meal_df.columns)
    empty_df.index = pd.DatetimeIndex([])
    
    # Test with empty DataFrame
    result_empty = erase_meal_overlap_fn(empty_df, meal_length, min_carbs)
    assert len(result_empty) == 0
    assert DataFrameValidator.validate_meal_df(result_empty)
    
    # Test with no meals above threshold
    high_min_carbs = 1000
    result_no_meals = erase_meal_overlap_fn(sample_meal_df, meal_length, high_min_carbs)
    assert DataFrameValidator.validate_meal_df(result_no_meals)
    
    # Test with invalid values
    with pytest.raises(ValueError):
        invalid_df = sample_meal_df.copy()
        invalid_df.loc[invalid_df.index[0], 'food_g'] = -1
        DataFrameValidator.validate_meal_df(invalid_df)