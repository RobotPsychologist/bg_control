import pandas as pd
from datetime import datetime
from itertools import product
from dataset_operations import (
    load_data,
    coerce_time_fn,
    dataset_label_modifier_fn,
    save_data,
    find_file_loc
)
from dataset_cleaner import (
    erase_consecutive_nan_values,
    erase_meal_overlap_fn,
    keep_top_n_carb_meals,
)
import os


def ensure_datetime_index(
        data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Ensures DataFrame has a datetime index.

    Parameters
    ----------
    data : pd.DataFrame
        Input DataFrame that either has a datetime index or a 'date' column
        that can be converted to datetime.

    Returns
    -------
    pd.DataFrame
        DataFrame with sorted datetime index.

    Raises
    ------
    ValueError
        If datetime conversion fails or if neither datetime index nor 'date' column exists.
    KeyError
        If 'date' column is not found in DataFrame.
    """
    # Make a copy to avoid modifying the original
    df = data.copy()

    # Check if the index is already a DatetimeIndex
    if not isinstance(df.index, pd.DatetimeIndex):
        # If not, set 'date' column as index and convert to DatetimeIndex
        if 'date' in df.columns:
            df = df.set_index('date')
        else:
            raise KeyError("DataFrame must have either a 'date' column or a DatetimeIndex.")

    # Ensure the index is a DatetimeIndex
    df.index = pd.DatetimeIndex(df.index)

    return df


def dataset_creator(
        raw_data_path='0_meal_identification/meal_identification/data/raw',
        output_dir='0_meal_identification/meal_identification/data/interim',
        use_auto_label=True,
        keep_cols=None,
        day_start_index_change=True,
        day_start_time=pd.Timedelta(hours=4),
        max_consecutive_nan_values_per_day=-1,
        min_carbs=5,
        n_top_carb_meals=3,
        meal_length=pd.Timedelta(hours=2),
        erase_meal_overlap=True,
        coerce_time=True,
        coerse_time_interval=pd.Timedelta(minutes=5),
        return_data=False,
        over_write=False,
):
    """
    Create a dataset from the raw data by orchestrating data loading, cleaning, transformation, and saving.

    Parameters
    ----------
    raw_data_path : str, optional
        Path to the directory containing raw data files (default is 'data/raw').
    output_dir : str, optional
        Directory to save the processed dataset (default is 'data/interim').
    use_auto_label : bool, optional
        Whether to use the auto label for the dataset (default is True).
    keep_cols : list of str, optional
        List of columns to keep from the raw data.
    day_start_index_change : bool, optional
        Whether to create a day index starting at a specific time.
    day_start_time : pd.Timedelta, optional
        The time of day to start the day index.
    max_consecutive_nan_values_per_day : int, optional
        Maximum number of consecutive NaN values allowed in a given day. If more than this number of consecutive NaN values are found in a day, then delete that day from the dataframe. Otherwise, delete the NaN values from that day.
        Set to a negative number (eg: -1) to disable this feature.
    min_carbs : int, optional
        Minimum amount of carbohydrates to consider a meal.
    n_top_carb_meals : int, optional
        Number of top carbohydrate meals to keep per day.
    meal_length : pd.Timedelta, optional
        Duration to consider for meal overlaps.
    erase_meal_overlap : bool, optional
        Whether to erase overlapping meals.
    coerce_time : bool, optional
        Whether to coerce the time intervals.
    coerse_time_interval : pd.Timedelta, optional
        Interval for coarse time.
    return_data : bool, optional
        Whether to return the processed data.
    over_write : False: bool, optional
        Whether to overwrite the processed dataset matching label already exists in the data/interim folder.

    Returns
    -------
    list of pd.DataFrame or None
        The processed DataFrames if `return_data` is True, else None.
    """
    if keep_cols is None:
        keep_cols = ['date', 'bgl', 'msg_type', 'affects_fob', 'affects_iob',
                     'dose_units', 'food_g', 'food_glycemic_index']

    # Load data using DatasetTransformer
    patient_dfs_dict = load_data(raw_data_path=raw_data_path, keep_cols=keep_cols)

    patient_dfs_list = [] if return_data else None

    for patient_key, patient_df in patient_dfs_dict.items():
        print(f"\n========================= \nProcessing: {patient_key[:6]}")
        label = dataset_label_modifier_fn(
            base_label_modifier="",
            coerce_time=True,
            coerce_time_interval=coerse_time_interval,
            day_start_index_change=True,
            day_start_time=day_start_time,
            erase_meal_overlap=True,
            min_carbs=min_carbs,
            meal_length=meal_length,
            n_top_carb_meals=n_top_carb_meals
        )
        time_stamp = datetime.today().strftime('%Y-%m-%d')

        if not over_write:
            filepath, filename = find_file_loc(
                output_dir=output_dir,
                data_label=label,
                patient_id=patient_key[:7],
                data_gen_date=time_stamp,
                include_gen_date_label=use_auto_label
            )
            if os.path.exists(filepath):
                print(f"File already exists at {filepath}, skipping save")
                continue

        patient_df = ensure_datetime_index(patient_df)

        # Coerce time intervals if required
        if coerce_time:
            patient_df = coerce_time_fn(data=patient_df, coerse_time_interval=coerse_time_interval)

        # Adjust day start index
        if day_start_index_change:
            patient_df['day_start_shift'] = (patient_df.index - day_start_time).date

        # Erase consecutive NaN values if max_consecutive_nan_values_per_day is set
        if max_consecutive_nan_values_per_day != -1:
            print(f"Erasing consecutive NaN values with max {max_consecutive_nan_values_per_day} per day")
            patient_df = erase_consecutive_nan_values(patient_df, max_consecutive_nan_values_per_day)

        # Erase meal overlaps
        if erase_meal_overlap:
            print(f"Erasing meal overlap with minCarb {min_carbs}g and {meal_length.components.hours}hr meal window")
            patient_df = erase_meal_overlap_fn(patient_df, meal_length, min_carbs)

        # Keep top N carbohydrate meals per day
        if n_top_carb_meals != -1:
            patient_df = keep_top_n_carb_meals(patient_df, n_top_carb_meals=n_top_carb_meals)

        # Save data with labeling
        save_data(
            data=patient_df,
            output_dir=output_dir,
            data_label=label if use_auto_label else 'dataLabelUnspecified_',
            patient_id=patient_key[:7],
            data_gen_date=time_stamp,
        )

        # Append to return list if required
        if return_data:
            patient_dfs_list.append(patient_df)

    print(f"\n\nAll data saved successfully in: {output_dir}")
    return patient_dfs_list


# This function is meant for generating new dataset only
def run_dataset_combinations(
    raw_data_path='0_meal_identification/meal_identification/data/raw',
    output_dir='0_meal_identification/meal_identification/data/interim',
    over_write=False
):
    """
    Run dataset_creator with different combinations of parameters
    """
    # Define parameter combinations
    min_carbs_options = [5, 10]
    meal_length_options = [2, 3, 5]  # hours
    n_top_meals_options = [3, 4]

    # Convert meal lengths to Timedelta
    meal_length_timedeltas = [pd.Timedelta(hours=h) for h in meal_length_options]

    # Create all combinations
    combinations = list(product(
        min_carbs_options,
        meal_length_timedeltas,
        n_top_meals_options
    ))

    # Run for each combination
    for min_carbs, meal_length, n_top_meals in combinations:
        print(f"\nProcessing combination:")
        print(f"- min_carbs: {min_carbs}g")
        print(f"- meal_length: {meal_length.components.hours}hrs")
        print(f"- n_top_meals: {n_top_meals}")

        try:
            dataset_creator(
                raw_data_path=raw_data_path,
                output_dir=output_dir,
                use_auto_label=True,
                day_start_index_change=True,
                day_start_time=pd.Timedelta(hours=4),
                min_carbs=min_carbs,
                n_top_carb_meals=n_top_meals,
                meal_length=meal_length,
                erase_meal_overlap=True,
                coerce_time=True,
                coerse_time_interval=pd.Timedelta(minutes=5),
                return_data=False,
                over_write=over_write
            )
            print("✓ Successfully processed combination")

        except Exception as e:
            print(f"✗ Error processing combination: {str(e)}")
            continue

    print("\nCompleted all combinations!")
