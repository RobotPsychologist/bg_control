import pandas as pd

def remove_num_meal(patient_df, num_meal):
    """
    Remove all days that have meals with the specified num_meal number of meals.

    Parameters
    ----------
    patient_df : pd.DataFrame
        The input DataFrame with columns 'msg_type', 'food_g', and a datetime index.
    num_meal : int
        The specific number of meals in a day to identify and remove.

    Returns
    -------
    pd.DataFrame
        The processed DataFrame with days containing num_meal meals removed.
    """
    # Ensure a 'day' column based on the date from the datetime index
    patient_df = patient_df.copy()
    patient_df['day'] = patient_df.index.date

    # Filter to only ANNOUNCE_MEAL rows
    announce_meal_df = patient_df[patient_df['msg_type'] == 'ANNOUNCE_MEAL']

    # Count the number of meals per day
    meal_counts = announce_meal_df.groupby('day').size()

    # Identify days with the specified number of meals
    days_to_remove = meal_counts[meal_counts == num_meal].index

    # Remove rows corresponding to these days
    result_df = patient_df[~patient_df['day'].isin(days_to_remove)]

    # Drop the temporary 'day' column
    result_df.drop(columns=['day'], inplace=True)

    return result_df
   

def erase_meal_overlap_fn(patient_df, meal_length, min_carbs):
    """
    Process the DataFrame to handle meal overlaps.

    Parameters
    ----------
    patient_df : pd.DataFrame
        The input DataFrame with columns 'msg_type', 'food_g', and a datetime index.
    meal_length : pd.Timedelta
        The duration to look ahead for meal events.
    min_carbs : int
        Minimum amount of carbohydrates to consider a meal.

    Returns
    -------
    pd.DataFrame
        The processed DataFrame with meal overlaps handled.
    """
    announce_meal_mask = patient_df['msg_type'] == 'ANNOUNCE_MEAL'
    announce_meal_indices = patient_df[announce_meal_mask].index

    for idx in announce_meal_indices:
        # Skip meals below the carbohydrate threshold
        if patient_df.at[idx, 'food_g'] <= min_carbs:
            patient_df.at[idx, 'msg_type'] = 'LOW_CARB_MEAL'
            continue

        # Define the time window
        window_end = idx + meal_length

        # Get the events within the time window, excluding the current event
        window_events = patient_df.loc[idx + pd.Timedelta(seconds=1):window_end]

        # Sum the 'food_g' counts greater than 0 within the window
        food_g_sum = window_events[window_events['food_g'] > 0]['food_g'].sum()

        # Add the sum to the original 'ANNOUNCE_MEAL' event
        patient_df.at[idx, 'food_g'] += food_g_sum

        # Erase the other events that fell within the window
        patient_df.loc[window_events.index, ['food_g', 'msg_type']] = [0, '']

    return patient_df


def keep_top_n_carb_meals(patient_df, n_top_carb_meals):
    """
    Keep only the top n carbohydrate meals per day in the DataFrame.

    Parameters
    ----------
    patient_df : pd.DataFrame
        The input DataFrame with columns 'msg_type', 'food_g', and a datetime index.
    n_top_carb_meals : int
        The number of top carbohydrate meals to keep per day.

    Returns
    -------
    pd.DataFrame
        The processed DataFrame with only the top n carbohydrate meals per day.
    """
    # Ensure 'day_start_shift' exists
    if 'day_start_shift' not in patient_df.columns:
        raise KeyError("'day_start_shift' column not found. Ensure day_start_index_change is True in dataset_creator.")

    # Filter the DataFrame to include only 'ANNOUNCE_MEAL' events
    announce_meal_df = patient_df[patient_df['msg_type'] == 'ANNOUNCE_MEAL'].copy()

    if announce_meal_df.empty:
        print("No 'ANNOUNCE_MEAL' events to process for top N meals.")
        return patient_df

    # Group by the shifted day
    grouped = announce_meal_df.groupby('day_start_shift')

    # Identify top n meal indices per group
    top_meal_indices = grouped.apply(lambda x: x.nlargest(n_top_carb_meals, 'food_g'), include_groups=False).index.get_level_values(1)

    # Mask to identify meals to keep
    keep_mask = patient_df.index.isin(top_meal_indices) & (patient_df['msg_type'] == 'ANNOUNCE_MEAL')

    # Set 'food_g' and 'msg_type' for non-top meals to 0 and '0' respectively
    patient_df.loc[~keep_mask & (patient_df['msg_type'] == 'ANNOUNCE_MEAL'), ['food_g', 'msg_type']] = [0, '0']

    return patient_df

def erase_consecutive_nan_values(patient_df: pd.DataFrame, max_consecutive_nan_values_per_day: int):
    """
    1. If there are more than max_consecutive_nan_values_per_day consecutive NaN values in a given day, then delete that day from the dataframe.
    2. If there are less than max_consecutive_nan_values_per_day consecutive NaN values in a given day, then delete the NaN values from that day.
    ------
    Parameters:
        patient_df: pd.DataFrame
            The input DataFrame with a datetime index.
        max_consecutive_nan_values_per_day: int
            The maximum number of consecutive NaN values allowed in a given day. If more than this number of consecutive NaN values are found in a day, then delete that day from the dataframe. Otherwise, delete the NaN values from that day.
    Returns:
        pd.DataFrame
            The processed DataFrame with consecutive NaN values handled.
    """
    # Create a copy to avoid modifying original
    df = patient_df.copy()
    
    # Add day column for grouping
    df['day'] = df.index.date
    
    # Process each day
    days_to_keep = []
    for day, day_data in df.groupby('day'):
        # Get boolean mask of NaN values
        nan_mask = day_data['bgl'].isnull()
        
        # Count consecutive NaNs
        consecutive_nans = 0
        max_consecutive = 0
        for is_nan in nan_mask:
            if is_nan:
                consecutive_nans += 1
                max_consecutive = max(max_consecutive, consecutive_nans)
            else:
                consecutive_nans = 0
                
        # Keep day if max consecutive NaNs is within limit
        if max_consecutive <= max_consecutive_nan_values_per_day:
            days_to_keep.append(day)
    
    # Filter to keep only valid days
    result_df = df[df['day'].isin(days_to_keep)].copy()
    
    # Drop the temporary day column
    result_df.drop('day', axis=1, inplace=True)
    
    # Drop remaining NaN values since they consecutively dont form a long enough chain
    result_df = result_df.dropna(subset=['bgl'])
    
    return result_df
