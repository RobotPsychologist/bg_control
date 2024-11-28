## Introduction

Managing and cleaning patient meal data is crucial for accurate analysis, especially in studies related to diabetes management, dietary impacts, and metabolic research. This toolkit offers robust functions to preprocess raw meal data, ensuring overlaps are handled, top carbohydrate meals are retained, and missing values are appropriately managed. Additionally, it provides utilities for dataset generation and visualization to aid researchers and data scientists in their workflows.

## Project Structure

The project is organized into several modules, each responsible for specific tasks:

- **dataset_cleaner.py**: Functions to clean and preprocess meal data.
- **dataset_generator.py**: Functions to generate and save processed datasets.
- **dataset_operations.py**: Core operations for loading, saving, and labeling data.
- **utils.py**: Utility functions for file handling and path management.
- **plots.py**: Visualization functions for analyzing meal data.

You can find these modules under `0_meal_identification/meal_identification/meal_identification/datasets`.


## Usage

### Dataset Cleaner

This module provides functions to clean and preprocess the raw meal data.



#### `erase_meal_overlap_fn`

**Purpose**: Handles overlapping meal events by merging them within a specified time window and applying carbohydrate thresholds.

**Parameters**:

- `patient_df` (`pd.DataFrame`): The input DataFrame containing at least `'msg_type'`, `'food_g'`, and a datetime index.
- `meal_length` (`pd.Timedelta`): Duration to look ahead for overlapping meal events.
- `min_carbs` (`int`): Minimum carbohydrate threshold to consider an event as a valid meal.

**Returns**:

- `pd.DataFrame`: Processed DataFrame with meal overlaps handled.

**Behaviour**:

1. Identifies all `'ANNOUNCE_MEAL'` events.
2. For each meal:
   - If `food_g` ≤ `min_carbs`, labels it as `'LOW_CARB_MEAL'`.
   - Otherwise, sums up `food_g` within the `meal_length` window and adds it to the original meal.
   - Erases overlapping events within the window by setting `'food_g'` to `0` and `'msg_type'` to an empty string.

#### `remove_num_meal`

**Purpose**: Removes all days that contain a specific number of meals (`ANNOUNCE_MEAL` events).

**Parameters**:

- `patient_df` (`pd.DataFrame`): The input DataFrame containing at least `'msg_type'`, `'food_g'`, and a datetime index.
- `num_meal` (`int`): The specific number of meals in a day to identify and remove.

**Returns**:

- `pd.DataFrame`: The processed DataFrame with days containing the specified number of meals removed.

**Behaviour**:

1. Extracts the date part of the datetime index and adds it as a temporary `'day'` column.
2. Filters to include only `'ANNOUNCE_MEAL'` events.
3. Groups the data by day and counts the number of meals per day.
4. Identifies days where the count of meals matches the specified `num_meal`.
5. Removes rows from the DataFrame corresponding to these identified days.
6. Drops the temporary `'day'` column.


#### `keep_top_n_carb_meals`

**Purpose**: Retains only the top N carbohydrate-rich meals per day, filtering out lesser meals.

**Parameters**:

- `patient_df` (`pd.DataFrame`): Input DataFrame with columns `'msg_type'`, `'food_g'`, and a datetime index. Must include `'day_start_shift'`.
- `n_top_carb_meals` (`int`): Number of top carbohydrate meals to retain per day.

**Returns**:

- `pd.DataFrame`: Processed DataFrame with only the top N carbohydrate meals per day retained.

**Behaviour**:

1. Verifies the existence of the `'day_start_shift'` column; raises a `KeyError` if absent.
2. Filters DataFrame to include only `'ANNOUNCE_MEAL'` events.
3. Groups meals by `'day_start_shift'` and selects the top N meals based on `'food_g'`.
4. Sets `'food_g'` to `0` and `'msg_type'` to `'0'` for meals not in the top N.


#### `erase_consecutive_nan_values`

**Purpose**: Manages consecutive missing (`NaN`) values in the dataset by either removing entire days or individual `NaN` entries based on specified thresholds.

**Parameters**:

- `patient_df` (`pd.DataFrame`): Input DataFrame with a datetime index.
- `max_consecutive_nan_values_per_day` (`int`): Maximum allowed consecutive `NaN` values per day. Days exceeding this threshold are removed entirely; otherwise, `NaN` values are dropped.

**Returns**:

- `pd.DataFrame`: Processed DataFrame with consecutive `NaN` values handled as per the threshold.

**Behaviour**:

1. Adds a temporary `'day'` column based on the date part of the datetime index.
2. Iterates through each day:
   - Counts the maximum number of consecutive `NaN` values in `'food_g'`.
   - If the maximum is within the allowed limit, retains the day; otherwise, excludes it.
3. Drops the temporary `'day'` column.
4. Removes remaining `NaN` values that do not form a long enough consecutive chain.

### Dataset Generator

This module orchestrates the dataset creation process, integrating loading, cleaning, transformation, and saving operations.

#### `ensure_datetime_index`

**Purpose**: Ensures that the DataFrame has a datetime index, either by verifying the existing index or converting a `'date'` column.

**Parameters**:

- `data` (`pd.DataFrame`): Input DataFrame that either has a datetime index or a `'date'` column.

**Returns**:

- `pd.DataFrame`: DataFrame with a sorted datetime index.

**Behaviour**:

1. Checks if the DataFrame's index is a `DatetimeIndex`.
2. If not, attempts to set the `'date'` column as the index.
3. Converts the index to a `DatetimeIndex`.
4. Sorts the DataFrame based on the datetime index.

**Notes**:

- **Docstring Accuracy**: The docstring correctly describes the function. However, it should clarify that the function **sets** the `'date'` column as the index if it's not already a `DatetimeIndex`.

#### `dataset_creator`

**Purpose**: Creates a processed dataset from raw data by applying various cleaning and transformation functions, then saves the result.

**Parameters**:

- `raw_data_path` (`str`, optional): Path to raw data files. Default: `'0_meal_identification/meal_identification/data/raw'`.
- `output_dir` (`str`, optional): Directory to save processed data. Default: `'0_meal_identification/meal_identification/data/interim'`.
- `use_auto_label` (`bool`, optional): Whether to use automatic labeling. Default: `True`.
- `keep_cols` (`list` of `str`, optional): Columns to retain from raw data. Default: `['date', 'bgl', 'msg_type', 'affects_fob', 'affects_iob', 'dose_units', 'food_g', 'food_glycemic_index']`.
- `day_start_index_change` (`bool`, optional): Whether to adjust day start index based on a specific time. Default: `True`.
- `day_start_time` (`pd.Timedelta`, optional): Time of day to start the day index. Default: `pd.Timedelta(hours=4)`.
- `max_consecutive_nan_values_per_day` (`int`, optional): Max allowed consecutive `NaN` values per day. Default: `-1` (disabled).
- `min_carbs` (`int`, optional): Minimum carbohydrates to consider a meal. Default: `5`.
- `n_top_carb_meals` (`int`, optional): Number of top carbohydrate meals to retain per day. Default: `3`.
- `meal_length` (`pd.Timedelta`, optional): Duration to consider for meal overlaps. Default: `pd.Timedelta(hours=2)`.
- `erase_meal_overlap` (`bool`, optional): Whether to handle meal overlaps. Default: `True`.
- `coerce_time` (`bool`, optional): Whether to coerce time intervals. Default: `True`.
- `coerse_time_interval` (`pd.Timedelta`, optional): Interval for time coercion. Default: `pd.Timedelta(minutes=5)`.
- `return_data` (`bool`, optional): Whether to return processed DataFrames. Default: `False`.
- `over_write` (`bool`, optional): Whether to overwrite existing processed datasets. Default: `False`.

**Returns**:

- `list` of `pd.DataFrame` or `None`: List of processed DataFrames if `return_data` is `True`; otherwise, `None`.

**Behaviour**:

1. **Data Loading**: Utilizes `load_data` to read raw CSV files from `raw_data_path`, retaining only specified columns.
2. **Processing Each Patient's Data**:
   - Ensures the DataFrame has a datetime index using `ensure_datetime_index`.
   - Applies time coercion if `coerce_time` is `True` via `coerce_time_fn`.
   - Adjusts day start index based on `day_start_time` if `day_start_index_change` is `True`.
   - Handles consecutive `NaN` values using `erase_consecutive_nan_values` if `max_consecutive_nan_values_per_day` is set.
   - Manages meal overlaps with `erase_meal_overlap_fn` if `erase_meal_overlap` is `True`.
   - Retains top N carbohydrate meals per day using `keep_top_n_carb_meals` if `n_top_carb_meals` is set.
3. **Saving Processed Data**: Saves the cleaned DataFrame using `save_data` with appropriate labeling.
4. **Handling Overwrites**: Skips saving if the file already exists and `over_write` is `False`.
5. **Returning Data**: Optionally appends processed DataFrames to a list for return if `return_data` is `True`.

**Notes**:

- **Docstring Accuracy**: The docstring mostly aligns with the function's Behaviour. However, there is a typo in the parameter description: `"over_write : False: bool, optional"` should be `"over_write : bool, optional"`.

#### `run_dataset_combinations`

**Purpose**: Generates datasets by iterating through various combinations of parameters to explore different preprocessing scenarios.

**Parameters**:

- `raw_data_path` (`str`, optional): Path to raw data files. Default: `'0_meal_identification/meal_identification/data/raw'`.
- `output_dir` (`str`, optional): Directory to save processed data. Default: `'0_meal_identification/meal_identification/data/interim'`.
- `over_write` (`bool`, optional): Whether to overwrite existing processed datasets. Default: `False`.

**Returns**:

- `None`

**Behaviour**:

1. **Parameter Combinations**: Defines ranges for `min_carbs` (5, 10), `meal_length` (2, 3, 5 hours), and `n_top_meals` (3, 4).
2. **Iteration**: For each combination, calls `dataset_creator` with the respective parameters.
3. **Error Handling**: Catches and logs any exceptions during processing, allowing the loop to continue with remaining combinations.
4. **Completion Message**: Prints a message upon completing all combinations.

### Dataset Operations

Core functions responsible for data loading, saving, labeling, and time coercion.

#### `get_root_dir`

**Purpose**: Determines the root directory of the project by searching for a unique identifier directory (e.g., `.github`).

**Parameters**:

- `current_dir` (`str`, optional): Starting directory for the search. Defaults to the current working directory if `None`.

**Returns**:

- `str`: Absolute path to the project root directory.

**Behaviour**:

1. Starts from `current_dir` or the current working directory.
2. Iteratively moves up the directory hierarchy.
3. Checks for the presence of the `unique_dir` (default `.github`) to identify the root.
4. Raises a `FileNotFoundError` if the root directory isn't found.


#### `load_data`

**Purpose**: Loads raw CSV data from the specified directory, retaining only specified columns.

**Parameters**:

- `raw_data_path` (`str`): Path to the directory containing raw CSV data files.
- `keep_cols` (`list` of `str`): Columns to retain from the raw data.

**Returns**:

- `dict`: Dictionary mapping filenames to their corresponding `pd.DataFrame` objects.

**Behaviour**:

1. Determines the full path to `raw_data_path` relative to the project root.
2. Validates the existence of the directory and the presence of CSV files.
3. Iterates through each CSV file, loading it into a DataFrame while retaining only `keep_cols`.
4. Handles and logs any errors encountered during file loading.
5. Returns a dictionary of loaded DataFrames.


#### `find_file_loc`

**Purpose**: Constructs the file path and filename for saving processed data based on provided parameters.

**Parameters**:

- `output_dir` (`str`): Directory to save the processed data.
- `data_label` (`str`): Label describing the dataset transformations.
- `patient_id` (`str`): Identifier for the patient.
- `data_gen_date` (`str`): Date when the data was generated (formatted as `'YYYY-MM-DD'`).
- `include_gen_date_label` (`bool`): Whether to include the generation date in the filename.

**Returns**:

- `tuple[str, str]`: Tuple containing the full file path and the filename.

**Behaviour**:

1. Determines the full path to `output_dir` relative to the project root and ensures the directory exists.
2. Constructs the filename based on whether `include_gen_date_label` is `True`:
   - If `True`: `"{data_gen_date}_{patient_id}_{data_label}.csv"`
   - If `False`: `"{patient_id}_{data_label}.csv"`
3. Returns the full file path and the filename.

#### `save_data`

**Purpose**: Saves the processed DataFrame to a CSV file in the specified directory with appropriate labeling.

**Parameters**:

- `data` (`pd.DataFrame`): The DataFrame to save.
- `output_dir` (`str`): Directory to save the data.
- `data_label` (`str`): Label describing the dataset transformations.
- `patient_id` (`str`): Identifier for the patient.
- `data_gen_date` (`str`): Date when the data was generated (formatted as `'YYYY-MM-DD'`).
- `include_gen_date_label` (`bool`, optional): Whether to include the generation date in the filename. Default: `True`.

**Returns**:

- `None`

**Behaviour**:

1. Calls `find_file_loc` to determine the full file path and filename.
2. Saves the DataFrame to the specified path using `to_csv`, including the datetime index.
3. Logs a success message with the file location and dataset label.

#### `dataset_label_modifier_fn`

**Purpose**: Generates a dataset label based on the transformations applied to the data, facilitating easy identification of preprocessing steps.

**Parameters**:

- `base_label_modifier` (`str`, optional): Base string to start the label. Default: `''`.
- `coerce_time` (`bool`, optional): Whether time intervals were coerced. Default: `False`.
- `coerce_time_interval` (`pd.Timedelta`, optional): Interval used for time coercion.
- `day_start_index_change` (`bool`, optional): Whether the day start index was adjusted based on a specific time. Default: `False`.
- `day_start_time` (`pd.Timedelta`, optional): Time of day when the day starts.
- `erase_meal_overlap` (`bool`, optional): Whether meal overlaps were handled. Default: `False`.
- `min_carbs` (`int`, optional): Minimum carbohydrate threshold used in overlap handling.
- `meal_length` (`pd.Timedelta`, optional): Duration considered for meal overlaps.
- `n_top_carb_meals` (`int`, optional): Number of top carbohydrate meals retained per day.

**Returns**:

- `str`: Modified dataset label reflecting the applied transformations.

**Behaviour**:

1. Starts with `base_label_modifier`.
2. Appends specific labels based on which transformations were applied:
   - Time coercion (`i{minutes}mins_`)
   - Day start index change (`d{hours}hrs_`)
   - Meal overlap handling (`c{min_carbs}g_l{hours}hrs_`)
   - Top N carbohydrate meals (`n{n_top_carb_meals}`)
3. Returns the concatenated label string.


#### `coerce_time_fn`

**Purpose**: Coerces the time intervals of the dataset to a specified frequency, ensuring consistent time steps.

**Parameters**:

- `data` (`pd.DataFrame`): Input DataFrame with a datetime index named `'date'`.
- `coerse_time_interval` (`pd.Timedelta`): Desired time interval for coercion.

**Returns**:

- `pd.DataFrame`: Coerced DataFrame with resampled time intervals.

**Behaviour**:

1. Validates that the DataFrame's index is named `'date'`; raises a `KeyError` if not.
2. Converts `coerse_time_interval` to a frequency string.
3. Separates meal announcements (`'ANNOUNCE_MEAL'`) from non-meal data.
4. Resamples non-meal data based on the specified frequency, taking the first entry in each bin.
5. Aligns meal announcements with the resampled non-meal data.
6. Combines the two DataFrames, ensuring meal announcements are retained.
7. Drops temporary columns used for merging.

### Utilities

#### `get_path`

**Purpose**: Infers the correct file path by ensuring the presence of a specified file suffix.

**Parameters**:

- `path` (`str` or `pathlib.Path`): The provided path or filename.
- `suffix` (`str`): The expected file extension (e.g., `'.csv'`).

**Returns**:

- `str`: Resolved file path with the appropriate suffix.

**Behaviour**:

1. Converts `path` to an absolute `Path` object.
2. Checks if the path has the specified suffix.
3. If not, verifies if a file with the original name exists.
4. If the file doesn't exist, appends the suffix to the path.
5. Returns the resolved path as a string.


### Plots

#### `plot_announce_meal_histogram`

**Purpose**: Visualizes the distribution of `'ANNOUNCE_MEAL'` events throughout the day, either by hour or in 15-minute intervals.

**Parameters**:

- `df` (`pd.DataFrame`): Input DataFrame containing `'msg_type'` and a datetime index.
- `hours_or_15minutes` (`str`, optional): Aggregation level for the histogram. Accepts `'hours'` or `'minutes'`. Default: `'hours'`.

**Returns**:

- `None`

**Behaviour**:

1. Filters the DataFrame to include only `'ANNOUNCE_MEAL'` events.
2. Extracts the hour and minute from each meal event's timestamp.
3. Depending on `hours_or_15minutes`:
   - **'minutes'**:
     - Converts time to fractional hours.
     - Plots a histogram with 15-minute interval bins (96 bins for 24 hours).
   - **'hours'**:
     - Plots a histogram with hourly bins (24 bins for 24 hours).
4. Configures plot aesthetics (labels, title, grid, layout).
5. Displays the histogram.
