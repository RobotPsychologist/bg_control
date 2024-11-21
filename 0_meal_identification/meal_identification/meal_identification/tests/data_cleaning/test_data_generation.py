# test_dataset_generator.py

import pytest
import pandas as pd
from datetime import timedelta
from unittest.mock import ANY

import sys
sys.path.append('0_meal_identification/meal_identification')
from unittest.mock import MagicMock

sys.modules['dataset_operations'] = MagicMock()
sys.modules['dataset_cleaner'] = MagicMock()

from meal_identification.datasets.dataset_generator import (
    ensure_datetime_index,
    dataset_creator,
    run_dataset_combinations
)

# Define fixtures for sample data
@pytest.fixture
def sample_data_with_date():
    return pd.DataFrame({
        'date': ['2023-01-01', '2023-01-02', '2023-01-03'],
        'value': [10, 20, 30]
    })

@pytest.fixture
def sample_data_with_datetime_index():
    return pd.DataFrame({
        'value': [10, 20, 30]
    }, index=pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03']))

@pytest.fixture
def sample_data_invalid_date():
    return pd.DataFrame({
        'date': ['invalid_date', '2023-01-02', '2023-01-03'],
        'value': [10, 20, 30]
    })

@pytest.fixture
def sample_data_no_date():
    return pd.DataFrame({
        'value': [10, 20, 30]
    })


def test_ensure_datetime_index_with_date_column(sample_data_with_date):
    """
    Objective: To verify that the ensure_datetime_index function correctly converts a DataFrame with a 'date' column into a DataFrame with a DatetimeIndex.
    Setup: Uses the sample_data_with_date fixture, which contains a 'date' column with valid date strings.
    Execution: Calls ensure_datetime_index with the sample data.
    Assertions:
    Checks if the resulting DataFrame's index is a pd.DatetimeIndex.
    Verifies that the index matches the expected datetime values.
    Ensures that the 'value' column remains unchanged and is correctly aligned with the new datetime index."""
    expected_index = pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03'])
    expected_index.name = 'date'  # Set the name to match the result
    result = ensure_datetime_index(sample_data_with_date)
    assert isinstance(result.index, pd.DatetimeIndex)
    pd.testing.assert_index_equal(result.index, expected_index)
    pd.testing.assert_series_equal(result['value'], pd.Series([10, 20, 30], index=expected_index, name='value'))


def test_ensure_datetime_index_with_datetime_index(sample_data_with_datetime_index):
    """
    Objective: To confirm that if a DataFrame already has a DatetimeIndex, the ensure_datetime_index function preserves it without alterations.
    
    Setup: Utilizes the sample_data_with_datetime_index fixture, which has a DatetimeIndex.
    Execution: Invokes ensure_datetime_index with this DataFrame.
    Assertions:
    Verifies that the index remains a pd.DatetimeIndex.
    Checks that the index values are as expected.
    Ensures the 'value' column remains correctly aligned with the index.
    """
    expected_index = pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03'])
    result = ensure_datetime_index(sample_data_with_datetime_index)
    assert isinstance(result.index, pd.DatetimeIndex)
    pd.testing.assert_index_equal(result.index, expected_index)
    pd.testing.assert_series_equal(result['value'], pd.Series([10, 20, 30], index=result.index, name='value'))

def test_ensure_datetime_index_missing_date_and_datetime_index(sample_data_no_date):
    """
    Objective: To ensure that the function raises a KeyError when the DataFrame lacks both a DatetimeIndex and a 'date' column.
    Mechanism:
    Setup: Uses the sample_data_no_date fixture, which lacks both a DatetimeIndex and a 'date' column.
    Execution & Assertion: Calls ensure_datetime_index within a context that expects a KeyError to be raised.
    """
    with pytest.raises(KeyError):
        ensure_datetime_index(sample_data_no_date)

def test_ensure_datetime_index_invalid_date_conversion(sample_data_invalid_date):
    """
    Objective: To verify that the function raises a ValueError when the 'date' column contains invalid date strings that cannot be converted to datetime objects.
    Mechanism:
    Setup: Employs the sample_data_invalid_date fixture, which includes an invalid date string.
    Execution & Assertion: Attempts to call ensure_datetime_index, expecting a ValueError due to the invalid date.
    """
    with pytest.raises(ValueError):
        ensure_datetime_index(sample_data_invalid_date)


# Mocking external dependencies using fixtures and the `mocker` fixture
@pytest.fixture
def mock_load_data(mocker):
    return mocker.patch('meal_identification.datasets.dataset_generator.load_data')

@pytest.fixture
def mock_dataset_label_modifier_fn(mocker):
    return mocker.patch('meal_identification.datasets.dataset_generator.dataset_label_modifier_fn')

@pytest.fixture
def mock_find_file_loc(mocker):
    return mocker.patch('meal_identification.datasets.dataset_generator.find_file_loc')

@pytest.fixture
def mock_save_data(mocker):
    return mocker.patch('meal_identification.datasets.dataset_generator.save_data')

@pytest.fixture
def mock_coerce_time_fn(mocker):
    return mocker.patch('meal_identification.datasets.dataset_generator.coerce_time_fn')

@pytest.fixture
def mock_erase_meal_overlap_fn(mocker):
    return mocker.patch('meal_identification.datasets.dataset_generator.erase_meal_overlap_fn')

@pytest.fixture
def mock_keep_top_n_carb_meals(mocker):
    return mocker.patch('meal_identification.datasets.dataset_generator.keep_top_n_carb_meals')

@pytest.fixture
def mock_os_path_exists(mocker):
    return mocker.patch('os.path.exists')

def test_dataset_creator_successful(
    mocker,
    mock_load_data,
    mock_dataset_label_modifier_fn,
    mock_find_file_loc,
    mock_os_path_exists,
    mock_save_data,
    mock_coerce_time_fn,
    mock_erase_meal_overlap_fn,
    mock_keep_top_n_carb_meals
):
    """
    
    Objective: To validate that dataset_creator successfully processes and saves data when all operations complete without issues.
    
    Mocking External Dependencies:
    load_data: Returns a sample DataFrame for a single patient.
    dataset_label_modifier_fn: Returns a fixed label 'test_label'.
    find_file_loc: Provides a fake file path and filename.
    os.path.exists: Simulates that the file does not already exist (False), allowing saving to proceed.
    Data Transformation Functions (coerce_time_fn, erase_meal_overlap_fn, keep_top_n_carb_meals): Configured to perform no operations, effectively passing the data through unchanged.
    
    Execution: Calls dataset_creator with mock paths and parameters, requesting the returned processed data.
    Assertions:
    Verifies that each mocked function is called exactly once with the expected arguments.
    Checks that the resulting list contains one DataFrame, confirming that data was processed and returned as expected.
    """
    # Setup mocks
    mock_load_data.return_value = {
        'patient_1': pd.DataFrame({
            'date': ['2023-01-01', '2023-01-02'],
            'bgl': [100, 110],
            'msg_type': ['A', 'B'],
            'affects_fob': [1, 2],
            'affects_iob': [3, 4],
            'dose_units': [5, 6],
            'food_g': [50, 60],
            'food_glycemic_index': [70, 80]
        })
    }
    
    mock_dataset_label_modifier_fn.return_value = 'test_label'
    mock_find_file_loc.return_value = ('/fake/path', 'fake_filename.csv')
    mock_os_path_exists.return_value = False
    mock_coerce_time_fn.side_effect = lambda data, coerse_time_interval: data  # No-op
    mock_erase_meal_overlap_fn.side_effect = lambda data, length, carbs: data
    mock_keep_top_n_carb_meals.side_effect = lambda data, n_top_carb_meals: data

    # Call dataset_creator
    result = dataset_creator(
        raw_data_path='fake/raw/path',
        output_dir='testing_output/dir',
        return_data=True,
        over_write=False
    )

    # Assertions
    mock_load_data.assert_called_once_with(raw_data_path='fake/raw/path', keep_cols=ANY)
    mock_dataset_label_modifier_fn.assert_called_once()
    mock_find_file_loc.assert_called_once()
    mock_os_path_exists.assert_called_once_with('/fake/path')
    mock_coerce_time_fn.assert_called_once()
    mock_erase_meal_overlap_fn.assert_called_once()
    mock_keep_top_n_carb_meals.assert_called_once()
    mock_save_data.assert_called_once()
    assert len(result) == 1
    assert isinstance(result[0], pd.DataFrame)

def test_dataset_creator_overwrite_false_file_exists(
    mocker,
    mock_load_data,
    mock_find_file_loc,
    mock_os_path_exists
):
    """
    Objective: To ensure that when overwrite=False and the target file already exists, dataset_creator skips processing and saving the data.
    Mocking:
    load_data: Returns sample data.
    find_file_loc: Provides a fake file location.
    os.path.exists: Simulates that the file already exists (True).
    
    Execution: Calls dataset_creator with overwrite=False.
    Assertions:
    Confirms that the function returns an empty list, indicating that processing was skipped due to the existing file.
    """
    # Setup mocks
    mock_load_data.return_value = {
        'patient_1': pd.DataFrame({
            'date': ['2023-01-01', '2023-01-02'],
            'bgl': [100, 110],
            'msg_type': ['A', 'B'],
            'affects_fob': [1, 2],
            'affects_iob': [3, 4],
            'dose_units': [5, 6],
            'food_g': [50, 60],
            'food_glycemic_index': [70, 80]
        })
    }
    mock_find_file_loc.return_value = ('/fake/path', 'fake_filename.csv')
    mock_os_path_exists.return_value = True  # File exists

    # Call dataset_creator
    result = dataset_creator(
        output_dir='fake/output/dir',
        return_data=True,
        over_write=False
    )

    # Assertions
    assert result == []

def test_dataset_creator_return_data_true(
    mocker,
    mock_load_data,
    mock_dataset_label_modifier_fn,
    mock_find_file_loc,
    mock_os_path_exists,
    mock_save_data,
    mock_coerce_time_fn,
    mock_erase_meal_overlap_fn,
    mock_keep_top_n_carb_meals
):
    """
    
    Objective: To verify that when return_data=True, dataset_creator correctly returns the processed DataFrame.
    Execution: Calls dataset_creator with return_data=True.
    Assertions:
    Ensures that the result is not None.
    Confirms that the returned list contains exactly one DataFrame.
    Checks that the returned object is indeed a pd.DataFrame.
    """
    # Setup mocks
    mock_load_data.return_value = {
        'patient_1': pd.DataFrame({
            'date': ['2023-01-01', '2023-01-02'],
            'bgl': [100, 110],
            'msg_type': ['A', 'B'],
            'affects_fob': [1, 2],
            'affects_iob': [3, 4],
            'dose_units': [5, 6],
            'food_g': [50, 60],
            'food_glycemic_index': [70, 80]
        })
    }
    mock_dataset_label_modifier_fn.return_value = 'test_label'
    mock_find_file_loc.return_value = ('/fake/path', 'fake_filename.csv')
    mock_os_path_exists.return_value = False
    mock_coerce_time_fn.side_effect = lambda data, coerse_time_interval: data
    mock_erase_meal_overlap_fn.side_effect = lambda data, length, carbs: data
    mock_keep_top_n_carb_meals.side_effect = lambda data, n_top_carb_meals: data

    # Call dataset_creator with return_data=True
    result = dataset_creator(
        raw_data_path='fake/raw/path',
        output_dir='fake/output/dir',
        return_data=True,
        over_write=False
    )

    # Assertions
    assert result is not None
    assert len(result) == 1
    assert isinstance(result[0], pd.DataFrame)

def test_dataset_creator_exception_handling(mocker, mock_load_data):
    """
    Objective: To ensure that dataset_creator properly propagates exceptions raised during the data loading phase.

    load_data: Configured to raise an Exception with the message "Load data failed".
    Execution & Assertion:
    Calls dataset_creator within a context expecting an Exception.
    Verifies that the raised exception contains the expected error message.
    """
    # Setup mock to raise an exception
    mock_load_data.side_effect = Exception("Load data failed")

    # Call dataset_creator and expect it to raise the exception
    with pytest.raises(Exception) as exc_info:
        dataset_creator(
            raw_data_path='fake/raw/path',
            output_dir='fake/output/dir',
            return_data=False,
            over_write=False
        )
    
    assert "Load data failed" in str(exc_info.value)

# # Step 6: Write tests for `run_dataset_combinations`

def test_run_dataset_combinations_success(mocker):
    """
    Objective: To verify that run_dataset_combinations correctly iterates over all parameter combinations and calls dataset_creator with the appropriate arguments.

    Execution: Calls run_dataset_combinations with mock paths.
    Assertions:
    Ensures that dataset_creator is called the expected number of times (12 in this case, considering all parameter combinations).
    Verifies that each call to dataset_creator includes the correct parameters corresponding to each combination.
    """
    # Mock itertools.product to return predefined combinations
    mock_product = mocker.patch('itertools.product')
    mock_product.return_value = [
        (5, timedelta(hours=2), 3),
        (5, timedelta(hours=2), 4),
        (5, timedelta(hours=3), 3),
        (5, timedelta(hours=3), 4),
        (10, timedelta(hours=2), 3),
        (10, timedelta(hours=2), 4),
        (10, timedelta(hours=3), 3),
        (10, timedelta(hours=3), 4),
    ]

    # Mock dataset_creator
    mock_dataset_creator = mocker.patch('meal_identification.datasets.dataset_generator.dataset_creator')

    # Call run_dataset_combinations
    run_dataset_combinations(
        raw_data_path='fake/raw/path',
        output_dir='fake/output/dir',
        over_write=False
    )

    # Assertions
    assert mock_dataset_creator.call_count == 12
    for combination in [
        (5, pd.Timedelta(hours=2), 3),
        (5, pd.Timedelta(hours=2), 4),
        (5, pd.Timedelta(hours=3), 3),
        (5, pd.Timedelta(hours=3), 4),
        (10, pd.Timedelta(hours=2), 3),
        (10, pd.Timedelta(hours=2), 4),
        (10, pd.Timedelta(hours=3), 3),
        (10, pd.Timedelta(hours=3), 4),
    ]:
        min_carbs, meal_length, n_top_meals = combination
        mock_dataset_creator.assert_any_call(
            raw_data_path='fake/raw/path',
            output_dir='fake/output/dir',
            use_auto_label=True,
            day_start_index_change=True,
            day_start_time=pd.Timedelta(hours=4),
            min_carbs=min_carbs,
            n_top_carb_meals=n_top_meals,
            meal_length=pd.Timedelta(hours=meal_length.seconds // 3600),
            erase_meal_overlap=True,
            coerce_time=True,
            coerse_time_interval=pd.Timedelta(minutes=5),
            return_data=False,
            over_write=False
        )
        
def test_run_dataset_combinations_with_exceptions(mocker):
    """
    Objective: To ensure that run_dataset_combinations gracefully handles exceptions raised during the processing of individual parameter combinations and continues processing subsequent combinations.
    Mechanism:
    Mocking:
    itertools.product: Mocked to return a single parameter tuple.
    dataset_creator: Configured to raise an Exception when called.
    print: Mocked to capture and verify the error message output.
    Execution: Invokes run_dataset_combinations with mock paths.
    Assertions:
    Confirms that dataset_creator is called exactly once.
    Checks that the appropriate error message ("✗ Error processing combination: Processing failed") is printed, indicating that the exception was caught and handled as expected.
    """
    # Mock product in the dataset_generator module
    mock_product = mocker.patch('meal_identification.datasets.dataset_generator.product')
    mock_product.return_value = [
        (5, pd.Timedelta(hours=2), 3),
    ]

    # Mock dataset_creator to raise an exception
    mock_dataset_creator = mocker.patch('meal_identification.datasets.dataset_generator.dataset_creator')
    mock_dataset_creator.side_effect = Exception("Processing failed")

    # Mock print to capture output
    mock_print = mocker.patch('builtins.print')

    # Call run_dataset_combinations
    run_dataset_combinations(
        raw_data_path='fake/raw/path',
        output_dir='fake/output/dir',
        over_write=False
    )

    # Assertions
    assert mock_dataset_creator.call_count == 1
    mock_print.assert_any_call("✗ Error processing combination: Processing failed")
