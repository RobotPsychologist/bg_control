from pydantic import BaseModel, ValidationError
import pandas as pd
from meal_identification.datasets.dataset_cleaner import remove_num_meal


class TestData(BaseModel):
    msg_type: list
    food_g: list
    timestamps: list

def test_remove_num_meal():
    # Mock data
    mock_data = TestData(
        msg_type=['ANNOUNCE_MEAL', 'ANNOUNCE_MEAL', 'ANNOUNCE_MEAL', 'OTHER', 'ANNOUNCE_MEAL', 'ANNOUNCE_MEAL'],
        food_g=[50, 60, 70, 0, 80, 90],
        timestamps=[
            '2024-11-01 08:00:00', '2024-11-01 08:05:00', '2024-11-01 08:10:00',
            '2024-11-01 08:15:00', '2024-11-02 08:00:00', '2024-11-02 08:05:00'
        ]
    )

    # Create DataFrame
    df = pd.DataFrame({
        'msg_type': mock_data.msg_type,
        'food_g': mock_data.food_g,
    }, index=pd.to_datetime(mock_data.timestamps))

    # Apply the function to remove days with 3 meals
    processed_df = remove_num_meal(df, num_meal=3)

    # Assert the correct days were removed
    # 2024-11-01 has 3 meals and should be removed
    # 2024-11-02 remains
    expected_timestamps = ['2024-11-02 08:00:00', '2024-11-02 08:05:00']
    expected_df = pd.DataFrame({
        'msg_type': ['ANNOUNCE_MEAL', 'ANNOUNCE_MEAL'],
        'food_g': [80, 90],
    }, index=pd.to_datetime(expected_timestamps))

    assert processed_df.equals(expected_df), f"Test failed: {processed_df} does not match {expected_df}"
