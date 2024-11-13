import os
import pandas as pd

def get_root_dir(current_dir=None):
    """
    Get the root directory of the project by looking for a specific directory 
    (e.g., '.github') that indicates the project root.

    Parameters
    ----------
    current_dir : str, optional
        The starting directory to search from. If None, uses the current working directory.

    Returns
    -------
    str
        The root directory of the project.
    """
    if current_dir is None:
        current_dir = os.getcwd()

    unique_dir = '.github'  # Directory that uniquely identifies the root

    while current_dir != os.path.dirname(current_dir):
        if os.path.isdir(os.path.join(current_dir, unique_dir)):
            return current_dir
        current_dir = os.path.dirname(current_dir)

    raise FileNotFoundError(f"Project root directory not found. '{unique_dir}' directory missing in path.")

def load_data(raw_data_path, keep_cols):
    """
    Load data from the raw data path.

    Parameters
    ----------
    raw_data_path : str
        Path to the directory containing raw data files.
    keep_cols : list of str
        List of columns to keep from the raw data.

    Returns
    -------
    dict
        A dictionary of DataFrames loaded from the raw data files.
    """
    project_root = get_root_dir()
    full_raw_loc_path = os.path.join(project_root, raw_data_path)
    
    if not os.path.exists(full_raw_loc_path):
        raise FileNotFoundError(f"Raw data path does not exist: {full_raw_loc_path}")

    csv_files = [f for f in os.listdir(full_raw_loc_path) if f.endswith('.csv')]
    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in the directory: {full_raw_loc_path}")

    dataframes = {}
    for file in csv_files:
        file_path = os.path.join(full_raw_loc_path, file)
        try:
            df = pd.read_csv(file_path, usecols=keep_cols, parse_dates=['date'])
            dataframes[file] = df
        except Exception as e:
            print(f"Error loading {file}: {e}")
    
    print("Loaded DataFrames:", list(dataframes.keys()))
    return dataframes

def save_data(data, output_dir, data_label, patient_id, data_gen_date, include_gen_date_label=True):
    """
    Save the data to the output directory.

    Parameters
    ----------
    data : pd.DataFrame
        The data to save
    output_dir : str
        The directory to save the data
    data_label : str
        The label for the data
    patient_id : str
        The patient ID
    data_gen_date : str
        The date the data was generated
    include_gen_date_label : bool
        Whether to include the data generation date in the label

    Returns
    -------
    None
    """
    project_root = get_root_dir()
    full_out_path_dir = os.path.join(project_root, output_dir)
    os.makedirs(full_out_path_dir, exist_ok=True)  # Ensure the output directory exists

    if include_gen_date_label:
        filename = f"{data_gen_date}_{patient_id}_{data_label}.csv"
    else:
        filename = f"{patient_id}_{data_label}.csv"

    file_path = os.path.join(full_out_path_dir, filename)
    data.to_csv(file_path, index=True)
    print(f"Data saved successfully in: {output_dir}")
    print(f"\n \t Dataset label: {filename}")

def dataset_label_modifier_fn(base_label_modifier,
                              coerce_time, coerce_time_label,
                              day_start_index_change, day_start_time_label,
                              erase_meal_overlap, erase_meal_label):
    """
    Modify the data label based on applied transformations.

    Parameters
    ----------
    base_label_modifier : str
        The base label modifier for the dataset
    coerce_time : bool
        Whether to coerce the time interval of the data
    coerce_time_label : str
        The label modifier for the time interval coercion
    day_start_index_change : bool
        Whether to create a day index starting at a specific time
    day_start_time_label : str
        The label modifier for the day start time
    erase_meal_overlap : bool
        Whether to erase overlapping meals
    erase_meal_label : str
        The label modifier for the meal overlap erasure

    Returns
    -------
    str
        The modified data label
    """
    data_label_modifier = base_label_modifier
    if coerce_time:
        data_label_modifier += coerce_time_label
    if day_start_index_change:
        data_label_modifier += day_start_time_label
    if erase_meal_overlap:
        data_label_modifier += erase_meal_label

    return data_label_modifier

def coerce_time_fn(data, coerse_time_interval):
    '''
    Coerce the time interval of the data.

    Parameters
    ----------
    data : pd.DataFrame
        The input DataFrame with a 'date' column.
    coerse_time_interval : pd.Timedelta
        The interval for coarse time resampling.

    Returns
    -------
    pd.DataFrame
        The coerced DataFrame with a DatetimeIndex.
    '''
    # Ensure 'date' column exists
    if 'date' not in data.columns:
        raise KeyError("'date' column not found in data.")

    # Convert 'date' to datetime if not already
    if not pd.api.types.is_datetime64_any_dtype(data['date']):
        data['date'] = pd.to_datetime(data['date'], errors='coerce')
        data = data.dropna(subset=['date'])  # Drop rows where 'date' couldn't be parsed

    # Set 'date' as the index without squeezing
    data = data.set_index('date').sort_index()

    # Define resample rule based on the provided timedelta
    resample_rule = f'{int(coerse_time_interval.total_seconds() // 60)}min'  # e.g., '5min' for 5 minutes

    # Resample the data
    data_resampled = data.resample(resample_rule).first()

    # Separate meal announcements and non-meal data
    meal_announcements = data_resampled[data_resampled['msg_type'] == 'ANNOUNCE_MEAL'].copy()
    non_meals = data_resampled[data_resampled['msg_type'] != 'ANNOUNCE_MEAL'].copy()

    # Resample meal announcements separately
    meal_announcements = meal_announcements.resample('5min').first()
    non_meals = non_meals.resample('5min').first()

    # Join the two DataFrames
    data_resampled = non_meals.join(meal_announcements, how='left', rsuffix='_meal')

    # Combine the columns
    for col in ['bgl', 'msg_type', 'food_g']:
        meal_col = f"{col}_meal"
        if meal_col in data_resampled.columns:
            data_resampled[col] = data_resampled[col + '_meal'].combine_first(data_resampled[col])
            data_resampled.drop(columns=[meal_col], inplace=True)

    # Retain 'food_g_keep' from meal announcements data_resampled = data.resample(resample_rule).first()
    data_resampled['food_g_keep'] = data_resampled.get('food_g_meal', 0)

    # Identify columns that end with '_meal'
    columns_to_drop = data_resampled.filter(regex='_meal$').columns

    # Drop the identified columns
    data_resampled = data_resampled.drop(columns=columns_to_drop)

    # At this point, 'date' is still the index. Do NOT reset the index.
    data_resampled['date'] = data_resampled.index

    print("Columns after coercing time:", data_resampled.columns.tolist())

    return data_resampled
