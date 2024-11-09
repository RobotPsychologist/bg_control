from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime
import pandas as pd

class MealRecord(BaseModel):
    """Pydantic model for validating individual meal records"""
    timestamp: datetime
    msg_type: str
    food_g: float
    day_start_shift: Optional[int] = None

    @validator('msg_type')
    def validate_msg_type(cls, v):
        valid_types = {'ANNOUNCE_MEAL', '', '0'}
        if v not in valid_types:
            raise ValueError(f'msg_type must be one of {valid_types}')
        return v

    @validator('food_g')
    def validate_food_g(cls, v):
        if v < 0:
            raise ValueError('food_g must be non-negative')
        return v

class DataFrameValidator:
    """Utility class for validating DataFrame structure and contents"""
    @staticmethod
    def validate_meal_df(df: pd.DataFrame) -> bool:
        """Validate DataFrame structure and contents"""
        # Check required columns
        required_columns = {'msg_type', 'food_g'}
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"DataFrame must contain columns: {required_columns}")

        # Validate index is datetime
        if not isinstance(df.index, pd.DatetimeIndex):
            raise ValueError("DataFrame must have DatetimeIndex")

        # Validate each row using MealRecord
        for idx, row in df.iterrows():
            MealRecord(
                timestamp=idx,
                msg_type=row['msg_type'],
                food_g=row['food_g'],
                day_start_shift=row.get('day_start_shift')
            )

        return True
