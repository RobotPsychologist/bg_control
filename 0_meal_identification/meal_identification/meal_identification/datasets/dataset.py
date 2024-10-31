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

    def coerce_time_fn():
        pass

    def erase_meal_overlap_fn():
        pass

    def keep_top_n_carb_meals_fn():
        pass






if __name__ == "__main__":
    app()
