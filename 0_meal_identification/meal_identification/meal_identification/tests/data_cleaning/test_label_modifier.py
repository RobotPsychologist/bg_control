import unittest
from datetime import timedelta, time
from dataclasses import dataclass
import pandas as pd
from meal_identification.datasets.dataset_operations import dataset_label_modifier_fn


class TestDatasetLabelModifier(unittest.TestCase):
    def setUp(self):
        """Set up test parameters that will be used in all tests"""
        self.base_label = "_base"
        # Create time objects for testing
        self.coerce_time_interval = pd.Timedelta(minutes=5)
        self.day_start_time = pd.Timedelta(hours=4)
        self.meal_length = pd.Timedelta(hours=2)
        self.min_carbs = 10
        self.n_top_meals = 3

    def test_no_modifications(self):
        """Test with no modifications enabled"""
        result = dataset_label_modifier_fn(
            base_label_modifier=self.base_label,
            coerce_time=False,
            coerce_time_interval=self.coerce_time_interval,
            day_start_index_change=False,
            day_start_time=self.day_start_time,
            erase_meal_overlap=False,
            min_carbs=self.min_carbs,
            meal_length=self.meal_length,
            n_top_carb_meals=self.n_top_meals
        )
        self.assertEqual(result, "_base" + f"n{self.n_top_meals}")

    def test_all_modifications(self):
        """Test with all modifications enabled"""
        result = dataset_label_modifier_fn(
            base_label_modifier=self.base_label,
            coerce_time=True,
            coerce_time_interval=self.coerce_time_interval,
            day_start_index_change=True,
            day_start_time=self.day_start_time,
            erase_meal_overlap=True,
            min_carbs=self.min_carbs,
            meal_length=self.meal_length,
            n_top_carb_meals=self.n_top_meals
        )
        expected = (f"_base"
                    f"i{5}mins_"
                    f"d{4}hrs_"
                    f"c{10}g_l{2}hrs_"
                    f"n{3}")
        self.assertEqual(result, expected)

    def test_only_coerce_time(self):
        """Test with only coerce time enabled"""
        result = dataset_label_modifier_fn(
            base_label_modifier=self.base_label,
            coerce_time=True,
            coerce_time_interval=self.coerce_time_interval,
            day_start_index_change=False,
            day_start_time=self.day_start_time,
            erase_meal_overlap=False,
            min_carbs=self.min_carbs,
            meal_length=self.meal_length,
            n_top_carb_meals=self.n_top_meals
        )
        expected = f"_basei{5}mins_n{3}"
        self.assertEqual(result, expected)

    def test_mixed_modifications(self):
        """Test with mixed modifications enabled"""
        result = dataset_label_modifier_fn(
            base_label_modifier=self.base_label,
            coerce_time=True,
            coerce_time_interval=self.coerce_time_interval,
            day_start_index_change=False,
            day_start_time=self.day_start_time,
            erase_meal_overlap=True,
            min_carbs=self.min_carbs,
            meal_length=self.meal_length,
            n_top_carb_meals=self.n_top_meals
        )
        expected = (f"_base"
                    f"i{5}mins_"
                    f"c{10}g_l{2}hrs_"
                    f"n{3}")
        self.assertEqual(result, expected)

    def test_empty_base_label(self):
        """Test with empty base label"""
        result = dataset_label_modifier_fn(
            base_label_modifier="",
            coerce_time=True,
            coerce_time_interval=self.coerce_time_interval,
            day_start_index_change=True,
            day_start_time=self.day_start_time,
            erase_meal_overlap=True,
            min_carbs=self.min_carbs,
            meal_length=self.meal_length,
            n_top_carb_meals=self.n_top_meals
        )
        expected = (f"i{5}mins_"
                    f"d{4}hrs_"
                    f"c{10}g_l{2}hrs_"
                    f"n{3}")
        self.assertEqual(result, expected)