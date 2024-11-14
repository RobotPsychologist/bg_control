from pydantic import BaseModel, Field, validator, confloat
from typing import List, Optional
from datetime import datetime
import pandas as pd

class MealRecord(BaseModel):
    """
    Pydantic model for validating individual meal records (i.e validate a single row of a dataframe)
    """
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


class RawMealRecord(BaseModel):
    date: datetime
    bgl: confloat(gt=0)
    msg_type: str

    @validator('msg_type')
    def validate_msg_type(cls, v):
        valid_types = {'ANNOUNCE_MEAL', 'DOSE_INSULIN', '', '0', }
        if v not in valid_types:
            raise ValueError(f'msg_type must be one of {valid_types}')
        return v

    @validator('bgl')
    def validate_bgl(cls, v):
        if v <= 20:
            raise ValueError('Blood glucose level must be positive')
        if v > 600:
            raise ValueError('Blood glucose level seems unreasonably high')
        return v

class DataFrameValidator:
    """A utility class for validating dataframe using a pydantic model for each row"""
    
    def __init__(self, model: type[BaseModel], index_field: str = 'timestamp'):
        """
        Initialize validator with a Pydantic model

        Parameters
        ----------
        model : type[BaseModel]
            Pydantic model class to use for validation on each row
        index_field : str, optional
            Name of the field in the model that corresponds to the index (default 'timestamp')
        """
        self.model = model
        self.index_field = index_field
        self.required_columns = {
            field_name for field_name, field in model.model_fields.items() 
            if field_name != index_field and field.is_required()
        }
        print(self.model.model_fields)
        self.index_is_datetime = self.model.model_fields[self.index_field].annotation == datetime

    def validate_df(self, df: pd.DataFrame, is_raw: bool = False) -> bool:
        """Validate DataFrame structure and contents"""
        # Check required columns
        if not all(col in df.columns for col in self.required_columns):
            raise ValueError(f"DataFrame must contain columns: {self.required_columns}")

        # Raw data's index is not datetime
        if not is_raw:
            # Validate index is datetime if model field is datetime
            if self.index_is_datetime and not isinstance(df.index, pd.DatetimeIndex):
                raise ValueError("DataFrame must have DatetimeIndex")

        # Validate each row using model
        for idx, row in df.iterrows():
            model_data = {field: row.get(field) for field in self.required_columns}
            model_data[self.index_field] = idx
            self.model(**model_data)

        return True
