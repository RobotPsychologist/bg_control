import pandas as pd
from datetime import datetime
from dataset_operations import (
    load_data,
    coerce_time_fn,
    dataset_label_modifier_fn,
    save_data,
)
from dataset_cleaner import (
    erase_meal_overlap_fn,
    keep_top_n_carb_meals,
)


def ensure_datetime_index(
        data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Ensures DataFrame has a datetime index.

    Parameters
    ----------
    data (pd.DataFrame): Input DataFrame

    Returns
    -------
    pd.DataFrame: DataFrame with datetime index

    Raises:
    -------
    ValueError: If datetime conversion fails or index column not found
    """
    df = data.copy()

    # Convert 'date' to datetime if not already
    if not pd.api.types.is_datetime64_any_dtype(df['date']):
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df = df.dropna(subset=['date'])  # Drop rows where 'date' couldn't be parsed

    # Set index if 'date' is still a column
    if 'date' in df.columns:
        df = df.set_index('date')

    # Sort index and ensure name is 'date'
    df = df.sort_index()

    return df


def dataset_creator(
        raw_data_path='0_meal_identification/meal_identification/data/raw',
        output_dir='0_meal_identification/meal_identification/data/interim',
        use_auto_label=True,
        keep_cols=None,
        day_start_index_change=True,
        day_start_time=pd.Timedelta(hours=4),
        min_carbs=10,
        n_top_carb_meals=3,
        meal_length=pd.Timedelta(hours=2),
        erase_meal_overlap=True,
        coerce_time=True,
        coerse_time_interval=pd.Timedelta(minutes=5),
        return_data=False,
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

        patient_df = ensure_datetime_index(patient_df)

        # Coerce time intervals if required
        if coerce_time:
            patient_df = coerce_time_fn(data=patient_df, coerse_time_interval=coerse_time_interval)

        # Adjust day start index
        if day_start_index_change:
            patient_df['day_start_shift'] = (patient_df.index - day_start_time).date

        # Erase meal overlaps
        if erase_meal_overlap:
            print(f"Erasing meal overlap with minCarb {min_carbs}g and {meal_length.components.hours}hr meal window")
            patient_df = erase_meal_overlap_fn(patient_df, meal_length, min_carbs)

        # Keep top N carbohydrate meals per day
        if n_top_carb_meals != -1:
            patient_df = keep_top_n_carb_meals(patient_df, n_top_carb_meals=n_top_carb_meals)

        # Save data with labeling
        if use_auto_label:
            label = dataset_label_modifier_fn(
                base_label_modifier='',
                coerce_time=coerce_time,
                coerce_time_label=f"timeInter{int(coerse_time_interval.total_seconds() // 60)}mins_",
                day_start_index_change=day_start_index_change,
                day_start_time_label=f"dayStart{day_start_time.components.hours}hrs_",
                erase_meal_overlap=erase_meal_overlap,
                erase_meal_label=f"minCarb{min_carbs}g_{meal_length.components.hours}hrMealW"
            )
            save_data(
                data=patient_df,
                output_dir=output_dir,
                data_label=label,
                patient_id=patient_key[:7],
                data_gen_date=datetime.today().strftime('%Y-%m-%d'),
                include_gen_date_label=True
            )
        else:
            save_data(
                data=patient_df,
                output_dir=output_dir,
                data_label='dataLabelUnspecified_',
                patient_id=patient_key[:7],
                data_gen_date=datetime.today().strftime('%Y-%m-%d'),
                include_gen_date_label=False
            )

        # Append to return list if required
        if return_data:
            patient_dfs_list.append(patient_df)

    print(f"\n\nAll data saved successfully in: {output_dir}")
    return patient_dfs_list
