from meal_identification.datasets.dataset_cleaner import keep_top_n_carb_meals
from meal_identification.datasets.pydantic_test_models import DataFrameValidator, MealRecord
from meal_identification.datasets.dataset_cleaner import erase_consecutive_nan_values


class TestDeleteConsecutiveNanValues:
    
    def validate_no_nan_values(self, noisy_df, max_consecutive_nan_values_per_day):
        """
        Tests that the outputted DataFrame has no NaN values
        """
        result_df = erase_consecutive_nan_values(noisy_df, max_consecutive_nan_values_per_day)
        assert not result_df.isnull().any().any()

    def test_more_than_max_consecutive_nan_values_per_day_deleted(self, noisy_df, max_consecutive_nan_values_per_day):
        """
        Tests that more than max_consecutive_nan_values_per_day consecutive NaN values are deleted
        """
        # Group data by day
        noisy_df['day'] = noisy_df.index.date
        grouped = noisy_df.groupby('day')
        
        # For each day, count consecutive NaN values
        days_with_too_many_nans = []
        for day, day_data in grouped:
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
                    
            if max_consecutive > max_consecutive_nan_values_per_day:
                days_with_too_many_nans.append(day)

        # then check that those days are deleted
        result_df = erase_consecutive_nan_values(noisy_df, max_consecutive_nan_values_per_day)
        # Just check that the days with too many consecutive NaNs are deleted
        assert not any(day in days_with_too_many_nans for day in result_df.index.date)

    def test_fewer_than_max_consecutive_nan_values_per_day_kept(self, noisy_df, max_consecutive_nan_values_per_day):
        """
        Tests that fewer than max_consecutive_nan_values_per_day consecutive NaN values are deleted
        """
        # First check which days have fewer than max_consecutive_nan_values_per_day consecutive NaN values
        noisy_df['day'] = noisy_df.index.date
        grouped = noisy_df.groupby('day')
        days_under_max_nans = []
        for day, day_data in grouped:
            nan_mask = day_data['bgl'].isnull()
            consecutive_nans = 0
            max_consecutive = 0
            for is_nan in nan_mask:
                if is_nan:
                    consecutive_nans += 1
                    max_consecutive = max(max_consecutive, consecutive_nans)
                else:
                    consecutive_nans = 0
                    
            if max_consecutive <= max_consecutive_nan_values_per_day:
                days_under_max_nans.append(day)

        print(days_under_max_nans)
        print(max_consecutive_nan_values_per_day)
        print("=========under max==========")
        # then check that those days are deleted
        result_df = erase_consecutive_nan_values(noisy_df, max_consecutive_nan_values_per_day)
        # Just check that all days in the resulting df has fewer than max_consecutive_nan_values_per_day consecutive NaN values
        assert all(day in days_under_max_nans for day in result_df.index.date)

