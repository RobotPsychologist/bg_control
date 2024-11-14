import pandas as pd
from meal_identification.datasets.dataset_operations import coerce_time_fn
import pytest

class TestCoerceTimeFn:
    def test_basic_functionality(self, df_to_coerce, coerce_interval):
        result = coerce_time_fn(df_to_coerce.copy(), coerce_interval)

        assert isinstance(result, pd.DataFrame)
        assert 'date' == result.index.name
        assert isinstance(result.index, pd.DatetimeIndex)

        # Check if the interval between timestamps is 5 minutes
        time_diffs = result.index.to_series().diff().dropna()
        assert all(diff == pd.Timedelta(minutes=5) for diff in time_diffs)

    def test_missing_date_column(self, df_to_coerce, coerce_interval):
        """Test behavior when date column is missing"""
        bad_data = df_to_coerce.copy().drop('date', axis=1)
        with pytest.raises(KeyError):
            coerce_time_fn(bad_data, coerce_interval)

    def test_meal_handling(self, df_to_coerce, coerce_interval):
        """Test proper handling of meal data"""
        result = coerce_time_fn(df_to_coerce.copy(), coerce_interval)

        # Check meal rows exist
        meal_rows = result[result['msg_type'] == 'ANNOUNCE_MEAL']
        assert len(meal_rows) > 0

        # Check food_g values are preserved for meals
        assert all(meal_rows['food_g'] > 0)
        assert all(meal_rows['food_g_keep'] > 0)

    def test_meal_announcement_handling(self, df_to_coerce, coerce_interval):
        """Test proper handling of meal announcements"""
        result = coerce_time_fn(df_to_coerce.copy(), coerce_interval)

        # Check if meal announcements are preserved
        meal_rows = result[result['msg_type'] == 'ANNOUNCE_MEAL']
        assert len(meal_rows) > 0

        # Check if food_g_keep is present and contains the right values
        assert 'food_g_keep' in result.columns
        assert all(result[result['msg_type'] == 'ANNOUNCE_MEAL']['food_g'] > 0)

    def test_column_preservation(self, df_to_coerce, coerce_interval):
        """Test if essential columns are preserved"""
        result = coerce_time_fn(df_to_coerce.copy(), coerce_interval)
        essential_columns = {'bgl', 'msg_type', 'food_g', 'food_g_keep'}
        assert essential_columns.issubset(set(result.columns))

    @pytest.mark.parametrize("interval", [pd.Timedelta(minutes=3),
                                          pd.Timedelta(minutes=5),
                                          pd.Timedelta(minutes=7),
                                          pd.Timedelta(seconds=30),
                                          pd.Timedelta(seconds=45),
                                          pd.Timedelta(hours=1)])
    def test_different_time_intervals(self, df_to_coerce, interval):
        """Test with different time intervals"""
        result = coerce_time_fn(df_to_coerce.copy(), interval)

        time_diffs = result.index.to_series().diff().dropna()
        assert all(diff == interval for diff in time_diffs), \
            f"Expected {interval} intervals but got different intervals."