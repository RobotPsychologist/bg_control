from pydantic import BaseModel, Field, validator, confloat, field_validator
from typing import List, Optional
from datetime import datetime
import pandas as pd

class NumericColumns(BaseModel):
    """
    Pydantic model for all numeric columns in the interim data
    """
    bgl: float
    dose_units: float
    food_g: float
    food_glycemic_index: float
    food_g_keep: float

    @field_validator('food_g')
    def validate_food_g(cls, v):
        if v < 0:
            raise ValueError('food_g must be non-negative')
        return v


class CategoricalColumns(BaseModel):
    """
    Pydantic model for all categorical columns in the interim data
    """
    date: datetime
    affects_fob: object
    day_start_shift: object
    msg_type: object
    affects_iob: object

    
class CosineTransformed(BaseModel):
    """
    Pydantic model for numerical data transformed by CosineTransformer
    """
    bgl: float
    dose_units: float
    food_g: float
    food_glycemic_index: float
    food_g_keep: float
    date: object
    affects_fob: object
    day_start_shift: object
    msg_type: object
    affects_iob: object
    

    @field_validator('bgl', 'dose_units', 'food_g', 'food_glycemic_index', 'food_g_keep')
    def validate_food_g(cls, v):
        if(v < -1 or v > 1):
            raise ValueError('Column value should be between -1 and 1')
        return v
    