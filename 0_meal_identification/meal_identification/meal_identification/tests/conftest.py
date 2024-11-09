import pytest
import pandas as pd
from datetime import datetime, timedelta

@pytest.fixture
def sample_meal_df():
    """Create a sample DataFrame for testing"""
    dates = pd.date_range(start='2024-01-01', periods=5, freq='H')
    data = {
        'msg_type': ['ANNOUNCE_MEAL', '', 'ANNOUNCE_MEAL', 'ANNOUNCE_MEAL', ''],
        'food_g': [50.0, 0.0, 30.0, 20.0, 0.0],
        'day_start_shift': [1, 1, 1, 2, 2]
    }
    return pd.DataFrame(data, index=dates)

@pytest.fixture
def meal_length():
    """Standard meal length for testing"""
    return pd.Timedelta(hours=2)

@pytest.fixture
def min_carbs():
    """Minimum carbs threshold for testing"""
    return 10