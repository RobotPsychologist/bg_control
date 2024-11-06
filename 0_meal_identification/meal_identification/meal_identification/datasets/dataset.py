from pathlib import Path

import typer
from loguru import logger
from tqdm import tqdm

from meal_identification.config import PROCESSED_DATA_DIR, RAW_DATA_DIR

app = typer.Typer()


@app.command()
def main(
    # ---- REPLACE DEFAULT PATHS AS APPROPRIATE ----
    input_path: Path = RAW_DATA_DIR / "dataset.csv",
    output_path: Path = PROCESSED_DATA_DIR / "dataset.csv",
    # ----------------------------------------------
):
    # ---- REPLACE THIS WITH YOUR OWN CODE ----
    logger.info("Processing dataset...")
    for i in tqdm(range(10), total=10):
        if i == 5:
            logger.info("Something happened for iteration 5.")
    logger.success("Processing dataset complete.")
    # -----------------------------------------


def raw_data_loader():
    '''file to memory, for raw data to in-memory representation of raw data.'''
    pass

def processed_data_loader():
    '''file to memory, for processed data to in-memory representation of processed data.'''
    pass

def processed_data_saver():
    '''memory to file, for processed data to in-memory representation of processed data.'''

    def dataset_label_modifier_fn():
        pass

    pass

def data_processor():
    '''data processing, for raw data to processed data.'''

    def coerce_time_fn(patient_df, coerse_time_interval):
        '''
        Coerce the time interval of the data
        '''
        patient_df = patient_df.set_index('date').squeeze()
        patient_df.index = pd.DatetimeIndex(patient_df.index)
        patient_df = patient_df.resample(coerse_time_interval).first()

        meal_annoucements_df = patient_df[patient_df['msg_type'] == 'ANNOUNCE_MEAL']
        meal_annoucements_df = meal_annoucements_df.resample('5min').first()
        non_meal_df = patient_df[patient_df['msg_type'] != 'ANNOUNCE_MEAL']
        non_meal_df = non_meal_df.resample('5min').first()

        patient_df_resampled = non_meal_df.join(meal_annoucements_df, how='left', rsuffix='_meal')

        patient_df_resampled['bgl'] = patient_df_resampled['bgl_meal'].combine_first(patient_df_resampled['bgl'])
        patient_df_resampled['msg_type'] = patient_df_resampled['msg_type_meal'].combine_first(patient_df_resampled['msg_type'])
        patient_df_resampled['food_g'] = patient_df_resampled['food_g_meal'].combine_first(patient_df_resampled['food_g'])
        patient_df_resampled['food_g_keep'] = patient_df_resampled['food_g_meal']
        # Identify columns that end with '_meal'
        columns_to_drop = patient_df_resampled.filter(regex='_meal$').columns

        # Drop the identified columns
        patient_df_resampled = patient_df_resampled.drop(columns=columns_to_drop)
        return patient_df_resampled

    def erase_meal_overlap_fn(patient_df, meal_length, min_carbs):
        '''
        Process the DataFrame to handle meal overlaps.

        Parameters
        ----------
        df : pd.DataFrame
            The input DataFrame with columns 'msg_type', 'food_g', and a datetime index.
        meal_length : pd.Timedelta
            The duration to look ahead for meal events.

        Returns
        -------
        pd.DataFrame
            The processed DataFrame with meal overlaps handled.
        '''

        announce_meal_indices = patient_df[patient_df['msg_type'] == 'ANNOUNCE_MEAL'].index
        patient_df[patient_df['msg_type'] == 'ANNOUNCE_MEAL']

        for idx in announce_meal_indices:
            # We do not want to consider meals that are less than the minimum carbs
            #   min carbs are okay if they are rolled into a larger meal, but they should
            #   not count as the start of a meal.
            if patient_df.at[idx, 'food_g'] <= min_carbs:
                 continue

            # Define the time window
            window_end = idx + meal_length

            # Get the events within the time window
            window_events = patient_df.loc[idx+pd.Timedelta(1):window_end]

            # Sum the 'food_g' counts greater than 0 within the window
            food_g_sum = window_events[window_events['food_g'] > 0]['food_g'].sum()

            # Add the sum to the original 'ANNOUNCE_MEAL' event
            patient_df.at[idx, 'food_g'] += food_g_sum

            # Erase the other events that fell within the window
            patient_df.loc[window_events.index[:], 'food_g'] = 0
            patient_df.loc[window_events.index[:], 'msg_type'] = ''

        return patient_df

    def keep_top_n_carb_meals_fn(patient_df, n_top_carb_meals):
        '''
        Keep only the top n carbohydrate meals per day in the DataFrame.

        Parameters
        ----------
        df : pd.DataFrame
            The input DataFrame with columns 'msg_type', 'food_g', and a datetime index.
        n_top_carb_meals : int
            The number of top carbohydrate meals to keep per day.

        Returns
        -------
        pd.DataFrame
            The processed DataFrame with only the top n carbohydrate meals per day.
        '''
        # Filter the DataFrame to include only 'ANNOUNCE_MEAL' events
        announce_meal_df = patient_df[patient_df['msg_type'] == 'ANNOUNCE_MEAL']

        # Group by date
        grouped = announce_meal_df.groupby('day_start_shift')
        # Initialize a list to store the indices of the top n meals
        top_meal_indices = []

        for date, group in grouped:
            # Sort the group by 'food_g' in descending order and keep the top n meals
            top_meals = group.nlargest(n_top_carb_meals, 'food_g')
            top_meal_indices.extend(top_meals.index)

        # Set the 'food_g' values of the other meals to 0
        patient_df.loc[~patient_df.index.isin(top_meal_indices) & (patient_df['msg_type'] == 'ANNOUNCE_MEAL'), 'food_g'] = 0
        patient_df.loc[~patient_df.index.isin(top_meal_indices) & (patient_df['msg_type'] == 'ANNOUNCE_MEAL'), 'msg_type'] = '0'
        return patient_df





if __name__ == "__main__":
    app()
