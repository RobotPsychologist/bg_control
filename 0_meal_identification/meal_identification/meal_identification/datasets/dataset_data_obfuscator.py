import pandas as pd
import numpy as np
from meal_identification.datasets.dataset_operations import get_root_dir
import os
from scipy.stats import gamma, norm
import random


def find_meals_threshold_daily(patient_df, target_meals_per_day=1.8):
    """
    Find threshold for food_g that results in target average meals per day. Default to 1.8 meal logged per day
    """
    meal_mask = patient_df['msg_type'] == 'ANNOUNCE_MEAL'
    daily_meals = patient_df[meal_mask].groupby(patient_df[meal_mask].index.date)
    avg_meals_per_day = daily_meals.size().mean()

    # Get percentile that would give us target meals per day
    target_percentile = (1 - (target_meals_per_day / avg_meals_per_day)) * 100
    threshold = np.percentile(patient_df[meal_mask]['food_g'], target_percentile)

    return threshold


def find_meals_threshold_weekly(patient_df, target_meals_per_week=3):
    """
    Find threshold for food_g that results in target average meals per week. Default to 3 meals logged per week
    """
    meal_mask = patient_df['msg_type'] == 'ANNOUNCE_MEAL'

    patient_df['week'] = patient_df.index.isocalendar().week
    weekly_meals = patient_df[meal_mask].groupby('week')
    avg_meals_per_week = weekly_meals.size().mean()

    target_percentile = (1 - (target_meals_per_week / avg_meals_per_week)) * 100
    threshold = np.percentile(patient_df[meal_mask]['food_g'], target_percentile)
    patient_df.drop('week', axis=1, inplace=True)

    return threshold


def process_largest_meals(patient_df, period="daily", threshold=None):
    """
    Process patient dataframe to keep meals above threshold while preserving original data.

    Args:
        patient_df: DataFrame with columns including 'msg_type', 'msg_meal_real', 'food_g'
        threshold: food_g threshold, if None will calculate to achieve 1.8 meals/day or 3 meals/week
        period: weekly or daily
    """

    # Calculate threshold if not provided
    if threshold is None:
        threshold = find_meals_threshold_daily(patient_df) if period == 'daily' else find_meals_threshold_weekly(
            patient_df)

    meal_mask = patient_df['msg_type'] == 'ANNOUNCE_MEAL'

    # Wipe out meals below threshold
    meals_to_remove = patient_df[meal_mask & (patient_df['food_g'] < threshold)].index
    patient_df.loc[meals_to_remove, 'msg_type_log'] = None

    return patient_df


def keep_daily_top_meal(patient_df):
    meal_mask = patient_df['msg_type'] == 'ANNOUNCE_MEAL'
    daily_meals = patient_df[meal_mask].groupby(patient_df[meal_mask].index.date)
    for date, day_meals in daily_meals:
        # Skip if no meals
        if len(day_meals) < 1:
            continue

        # Find the largest meal for the day
        largest_meal_idx = day_meals['food_g'].idxmax()

        # Wipe all meals except the largest
        meals_to_remove = day_meals.index[day_meals.index != largest_meal_idx]
        patient_df.loc[meals_to_remove, 'msg_type_log'] = None

    return patient_df


def logging_behaviour_obfuscator(
        patient_df: pd.DataFrame,
        logger_type,
        distribution=None
):
    """
    Parameters
    ----------
    patient_df: patient dataframe to obfuscate
    logger_type: number representing type of logger the patient is based on the distribution param
    distribution: ranges for different types of meal logging behavior
     - First range: All meals
     - Second range: Multiple meals per day (1-2 largest meals)
     - Third range: Once per day (largest meal)
     - Fourth range: A few times per week
     - Fifth range: Never
     Default to [0, 0.20, 0.45, 0.65, 0.85, 1]
    Returns
    -------
    tuple(patient_df, logger_type)
    """
    if distribution is None:
        distribution = [0, 0.20, 0.45, 0.65, 0.85, 1]

    patient_df['msg_type_log'] = patient_df['msg_type']
    if distribution[0] <= logger_type < distribution[1]:
        # Type 1: Log all meals
        # Do nothing - keep all logs
        return patient_df, "full"

    elif distribution[1] <= logger_type < distribution[2]:
        # Type 2: Log 1-2 largest meals per day (default to 1.8 logs/day)
        patient_df = process_largest_meals(patient_df, period="daily")
        return patient_df, "top2"

    elif distribution[2] <= logger_type < distribution[3]:
        # Type 3: Log once per day (largest meal)
        patient_df = keep_daily_top_meal(patient_df)
        return patient_df, "once"

    elif distribution[3] <= logger_type < distribution[4]:
        # Type 4: Log a few times per week (default to 3 logs/week)
        patient_df = process_largest_meals(patient_df, period="weekly")
        return patient_df, "weekly"

    elif distribution[4] <= logger_type <= distribution[5]:
        # Type 5: Never log meals
        patient_df['msg_type_log'] = None
        return patient_df, "none"


def generate_meal_logging_distribution(direction='right'):
    """
    Generate distribution parameters with internal direction handling randomly.
    TODO: Spread should be params
    Parameters
    ----------
    direction: 'right', 'left', or 'normal'

    Returns
    -------
    For normal: (mean, std, distribution_object)
    For skewed: (shape, scale, offset, distribution_object)
    """
    if direction == 'normal':
        mean = random.uniform(-15, 15)  # TODO: Should be a param
        std = random.uniform(8, 12)  # TODO: Should be a param
        return mean, std, norm(mean, std)

    else:
        if direction == 'left':  # hasty logger (early)
            # More conservative parameters for early logging
            shape = random.uniform(2.5, 3.5)  # TODO: Should be a param
            scale = random.uniform(2, 3)      # TODO: Should be a param
            offset = random.uniform(-8, -5)          # TODO: Should be a param

        else:  # right skew - forgetful logger (late)
            # More extreme parameters for late logging
            shape = random.uniform(1.5, 2.5)  # TODO: Should be a param
            scale = random.uniform(4, 6)      # TODO: Should be a param
            offset = random.uniform(5, 10)    # TODO: Should be a param

        return shape, scale, offset


def shift_meals(patient_df, direction='right'):
    """
    Simulates different meal logging behaviors by shifting meal announcement times based on specified patterns.

    This function processes meal announcements in a patient's time series data and shifts them according to
    different logging behavior patterns: normal (symmetric), hasty (left-skewed), or forgetful (right-skewed).

    Parameters
    ----------
    patient_df : pd.DataFrame
        DataFrame with patient data, must have:
        - 'date'
        - 'msg_type_log' column containing 'ANNOUNCE_MEAL' entries from logging_behaviour_obfuscator()

    direction : str, default='right'
        The type of logging behavior to simulate:
        - 'normal': Symmetric shifts around actual meal times
        - 'left': Hasty logger who tends to log before meals
        - 'right': Forgetful logger who tends to log after meals

    Returns
    -------
    pd.DataFrame
        Copy of input DataFrame with new column 'msg_type_log_shifted' containing the shifted meal announcements.
        Non-meal entries will have None values.

    Notes
    -----
    - For normal loggers, shifts are drawn from a normal distribution
    - For hasty/forgetful loggers, shifts are drawn from a gamma distribution
    - Shifts that would move meals outside the time series range are ignored
    - New meal times are snapped to the nearest existing time index
    """

    patient_df['msg_type_log_shifted'] = None
    meal_times = patient_df[patient_df['msg_type_log'] == 'ANNOUNCE_MEAL'].index

    # Shift each meal time with random sampling from the distribution
    for meal_time in meal_times:
        # Generate new parameters for each meal
        if direction == 'normal':
            mean, std, _ = generate_meal_logging_distribution(direction)
            min_to_shift = np.random.normal(mean, std)
        else:
            shape, scale, offset = generate_meal_logging_distribution(direction)
            raw_sample = gamma.rvs(a=shape, scale=scale)
            median = shape * scale * (1 - 2 / (9 * shape)) ** 3

            if direction == 'left':
                # hasty logger
                # min_to_shit: Mean - Median < 0
                min_to_shift = (raw_sample + gamma.ppf(0.05, a=shape, scale=scale) + offset) - median / 2

            else:
                # forgetful logger
                #  min_to_shit: Mean - Median > 0
                min_to_shift = (raw_sample + gamma.ppf(0.01, a=shape, scale=scale) + offset) - median

        # Shift the meal
        new_time = meal_time + pd.Timedelta(minutes=min_to_shift)
        if patient_df.index.min() <= new_time <= patient_df.index.max():
            nearest_time = patient_df.index[patient_df.index.get_indexer([new_time], method='nearest')[0]]
            patient_df.loc[nearest_time, 'msg_type_log_shifted'] = 'ANNOUNCE_MEAL'

    return patient_df


def logging_timing_obfuscator(
        patient_df: pd.DataFrame,
        logger_timeing,
        distribution=None
):
    """
    Parameters
    ----------
    patient_df: patient dataframe to obfuscate
    logger_timeing: number representing type of logger the patient is based on the distribution param
    distribution: ranges for different types of meal logging timing
     - First range: Temporally right skewed -> forgetful loggers
     - Second range: Temporally left skewed -> hasty loggers
     - Third range:  Normal Distribution
     - Fourth range: Unchanged
     Default to [0, 0.38, 0.61, 0.89, 1]
    Returns
    -------
    tuple(patient_df, logger_type)
    """
    if distribution is None:
        distribution = [0, 0.38, 0.61, 0.89, 1]

    # Should be working with `msg_type_log` column from meal_logging_obfuscator
    if distribution[0] <= logger_timeing < distribution[1]:
        # Type 1: Temporally right skewed
        patient_df = shift_meals(patient_df, "right")
        return patient_df, "forgetful"

    elif distribution[1] <= logger_timeing < distribution[2]:
        # Type 2: Temporally left skewed
        patient_df = shift_meals(patient_df, "left")
        return patient_df, "hasty"

    elif distribution[2] <= logger_timeing < distribution[3]:
        # Type 3: Normal Distribution (28%)
        patient_df = shift_meals(patient_df, "normal")
        return patient_df, "normal"

    elif distribution[3] <= logger_timeing < distribution[4]:
        patient_df['msg_type_log_shifted'] = patient_df['msg_type_log']
        return patient_df, "unchanged"


def start():
    project_root = get_root_dir()
    sim_dir = os.path.join(project_root, '0_meal_identification', 'meal_identification', 'data', 'raw', 'sim')
    processed_dir = os.path.join(project_root, '0_meal_identification', 'meal_identification', 'data', 'raw',
                                 'obfuscated')

    # TODO: Need to figure out why some files from data/raw/sim have a new line character at the end
    csv_files = [f for f in os.listdir(sim_dir) if f.endswith('.csv')]


    patient_count = len(csv_files)

    print("Total patients: {}".format(patient_count))

    # Ranges for different types of meal logging behavior
    uniform_dist_logging_behaviour = np.random.uniform(0, 1, patient_count)
    distribution_logging_behaviour = [0, 0.20, 0.45, 0.65, 0.85, 1]

    # Ranges for different types of meal logging timing
    uniform_dist_logging_timing = np.random.uniform(0, 1, patient_count)
    distribution_logging_timing = [0, 0.38, 0.61, 0.89, 1]

    processed_count = 0

    for idx, file in enumerate(csv_files):
        # Randomly assign a patient to a type of logger based on uniform distribution
        logger_type = uniform_dist_logging_behaviour[idx]
        logger_timeing = uniform_dist_logging_timing[idx]

        file_path = os.path.join(sim_dir, file)
        try:
            df = pd.read_csv(file_path, parse_dates=['date']).drop('Unnamed: 0', axis=1)
            df = df.set_index('date')
            df.index = pd.DatetimeIndex(df.index)

            # Simulate logging behaviour
            patient_df, logger_type = logging_behaviour_obfuscator(df, logger_type, distribution_logging_behaviour)

            # Simulate logging timing
            patient_df, logger_timeing = logging_timing_obfuscator(patient_df, logger_timeing, distribution_logging_timing)

            # Remove old .csv extension
            file = file.replace('.csv', '')
            file = f"{file}_{logger_type}_{logger_timeing}.csv"
            output_file = os.path.join(processed_dir, file)
            df = df.reset_index()
            df.to_csv(output_file, index=True)

            print(f"Successfully processed and saved {file}")
            processed_count += 1

        except Exception as e:
            print(f"Error processing {file}: {str(e)}")

    print(f"Total file processed: {processed_count}")


if __name__ == '__main__':
    start()
