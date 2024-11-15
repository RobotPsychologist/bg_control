from meal_identification.datasets.dataset_cleaner import keep_top_n_carb_meals
from meal_identification.datasets.pydantic_test_models import DataFrameValidator, MealRecord

class TestKeepTopNMeals:
    def test_validate_structure(self, sample_meal_df, n_top_carb_meals):
        """
        Test that the output DataFrame maintains valid structure via pydantic
        """
        result_df = keep_top_n_carb_meals(sample_meal_df, n_top_carb_meals)
        assert DataFrameValidator(MealRecord).validate_df(result_df)

    def test_top_n_carbs_kept(self, sample_meal_df, n_top_carb_meals):
        """
        Tests that the top n carbohydrate meals are kept in a particular day
        """
        result_df = keep_top_n_carb_meals(sample_meal_df, n_top_carb_meals)
        
        # Group meals by day
        original_meals = sample_meal_df[sample_meal_df['msg_type'] == 'ANNOUNCE_MEAL']
        grouped_original = original_meals.groupby('day_start_shift')
        
        # For each day, check that the kept meals are the top n by carbs
        for day, day_meals in grouped_original:
            top_n_carbs = day_meals.nlargest(n_top_carb_meals, 'food_g')['food_g'].values
            kept_meals = result_df[
                (result_df['day_start_shift'] == day) & 
                (result_df['msg_type'] == 'ANNOUNCE_MEAL')
            ]['food_g'].values
            
            assert len(kept_meals) <= n_top_carb_meals
            assert all(carb in top_n_carbs for carb in kept_meals)

    def test_top_carbs_meals_kept_in_order(self, sample_meal_df, n_top_carb_meals):
        """
        Tests that in a day, the top N carb meals are kept in order
        """
        result_df = keep_top_n_carb_meals(sample_meal_df, n_top_carb_meals)
        
        # Group meals by day
        original_meals = sample_meal_df[sample_meal_df['msg_type'] == 'ANNOUNCE_MEAL']
        grouped_original = original_meals.groupby('day_start_shift')
        
        # For each day, check that the kept meals are in order
        for day, day_meals in grouped_original:
            kept_meals = result_df[
                (result_df['day_start_shift'] == day) & 
                (result_df['msg_type'] == 'ANNOUNCE_MEAL')
            ]['food_g'].values
            assert all(kept_meals == day_meals.nlargest(n_top_carb_meals, 'food_g')['food_g'].values)
