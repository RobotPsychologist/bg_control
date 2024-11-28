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

def find_file_loc(output_dir, data_label, patient_id, data_gen_date, include_gen_date_label=True):
    """
    Find the directory with given output directory

    Parameters
    ----------
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
   tuple[str, str]
        A tuple containing (full_path, filename)
        full_path: complete path to the file
        filename: just the filename portion
    """
    project_root = get_root_dir()
    full_out_path_dir = os.path.join(project_root, output_dir)
    os.makedirs(full_out_path_dir, exist_ok=True)  # Ensure the output directory exists

    if include_gen_date_label:
        filename = f"{data_gen_date}_{patient_id}_{data_label}.csv"
    else:
        filename = f"{patient_id}_{data_label}.csv"

    return os.path.join(full_out_path_dir, filename), filename

def save_data(data, output_dir, data_label, patient_id, data_gen_date):
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

    Returns
    -------
    None
    """

    file_path, filename = find_file_loc(output_dir, data_label, patient_id, data_gen_date, include_gen_date_label=True)
    data.to_csv(file_path, index=True)
    print(f"Data saved successfully in: {output_dir}")
    print(f"\n \t Dataset label: {filename}")


def dataset_label_modifier_fn(
        base_label_modifier='',
        coerce_time=False,
        coerce_time_interval=None,
        day_start_index_change=False,
        day_start_time=None,
        erase_meal_overlap=False,
        min_carbs=None,
        meal_length=None,
        n_top_carb_meals=None
):
    """
    Modify the data label based on applied transformations.

    Parameters
    ----------
    base_label_modifier : str, optional
        The base label modifier for the dataset
    coerce_time : bool, optional
        Whether to coerce the time interval of the data
    coerce_time_interval : timedelta, optional
        Time interval for coercion
    day_start_index_change : bool, optional
        Whether to create a day index starting at a specific time
    day_start_time : pd.Timedelta, optional
        Time object specifying when the day starts
    erase_meal_overlap : bool, optional
        Whether to erase overlapping meals
    min_carbs : int, optional
        Minimum carbs threshold for meal detection
    meal_length : pd.Timedelta, optional
        Length of time for meal window
    n_top_carb_meals : int, optional
        Number of top carb meals to consider

    Returns
    -------
    str
        The modified data label
        i: interval in minutes
        d: day_start in hours
        c: min_carbs in g
        l: meal_length in minutes
        n: n_top_carb_meals in g
    """
    data_label_modifier = base_label_modifier

    if coerce_time and coerce_time_interval is not None:
        minutes = int(coerce_time_interval.total_seconds() // 60)
        data_label_modifier += f"i{minutes}mins_"

    if day_start_index_change and day_start_time is not None:
        data_label_modifier += f"d{day_start_time.components.hours}hrs_"

    if erase_meal_overlap and min_carbs is not None and meal_length is not None:
        data_label_modifier += f"c{min_carbs}g_l{meal_length.components.hours}hrs_"

    if n_top_carb_meals is not None:
        data_label_modifier += f"n{n_top_carb_meals}"

    return data_label_modifier

def coerce_time_fn(data, coerse_time_interval):
    '''
    Coerce the time interval of the data.

    Parameters
    ----------
    data : pd.DataFrame
        The input DataFrame with a 'date' index.
    coerse_time_interval : pd.Timedelta
        The interval for coarse time resampling.

    Returns
    -------
    pd.DataFrame
        The coerced DataFrame with a DatetimeIndex.
    '''
    # Ensure 'date' column exists
    if 'date' != data.index.name:
        raise KeyError(f"'date' column should be index, got {data.index.name} instead")

    if not isinstance(coerse_time_interval, pd.Timedelta):
        raise TypeError(
            f"coerse_time_interval must be a pandas Timedelta object, got {type(coerse_time_interval)} instead")

    # Convert Timedelta directly to frequency string
    freq = pd.tseries.frequencies.to_offset(coerse_time_interval)

    # Separate meal announcements and non-meal data
    meal_announcements = data[data['msg_type'] == 'ANNOUNCE_MEAL'].copy()
    non_meals = data[data['msg_type'] != 'ANNOUNCE_MEAL'].copy()

    non_meals = non_meals.resample(freq).first()
    start_time = non_meals.index.min()

    # Resample meal announcements separately and align with non_meal
    meal_announcements = meal_announcements.resample(freq, origin=start_time).first()

    # Join the two DataFrames
    data_resampled = non_meals.join(meal_announcements, how='left', rsuffix='_meal')

    # Combine the columns
    for col in ['bgl', 'msg_type', 'food_g']:
        meal_col = f"{col}_meal"
        if meal_col in data_resampled.columns:
            data_resampled[col] = data_resampled[col + '_meal'].combine_first(data_resampled[col])

    # Retain 'food_g_keep' from meal announcements data_resampled = data.resample(resample_rule).first()
    data_resampled['food_g_keep'] = data_resampled.get('food_g_meal', 0)

    # Identify columns that end with '_meal'
    columns_to_drop = data_resampled.filter(regex='_meal$').columns

    # Drop the identified columns
    data_resampled = data_resampled.drop(columns=columns_to_drop)

    print("Columns after coercing time:", data_resampled.columns.tolist())

    return data_resampled
