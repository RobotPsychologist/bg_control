import unittest
from meal_identification.datasets.dataset_operations import dataset_label_modifier_fn

class TestDatasetLabelModifier(unittest.TestCase):
    def setUp(self):
        """Set up test parameters that will be used in all tests"""
        self.base_label = "_base"
        self.coerce_label = "_timeInter5mins"
        self.day_start_label = "_dayStart4hrs"
        self.erase_meal_label = "_minCarb10g"

    def test_no_modifications(self):
        """Test with no modifications enabled"""
        result = dataset_label_modifier_fn(
            base_label_modifier=self.base_label,
            coerce_time=False,
            coerce_time_label=self.coerce_label,
            day_start_index_change=False,
            day_start_time_label=self.day_start_label,
            erase_meal_overlap=False,
            erase_meal_label=self.erase_meal_label
        )
        self.assertEqual(result, "_base")

    def test_all_modifications(self):
        """Test with all modifications enabled"""
        result = dataset_label_modifier_fn(
            base_label_modifier=self.base_label,
            coerce_time=True,
            coerce_time_label=self.coerce_label,
            day_start_index_change=True,
            day_start_time_label=self.day_start_label,
            erase_meal_overlap=True,
            erase_meal_label=self.erase_meal_label
        )
        self.assertEqual(result, "_base_timeInter5mins_dayStart4hrs_minCarb10g")

    def test_only_coerce_time(self):
        """Test with only coerce time enabled"""
        result = dataset_label_modifier_fn(
            base_label_modifier=self.base_label,
            coerce_time=True,
            coerce_time_label=self.coerce_label,
            day_start_index_change=False,
            day_start_time_label=self.day_start_label,
            erase_meal_overlap=False,
            erase_meal_label=self.erase_meal_label
        )
        self.assertEqual(result, "_base_timeInter5mins")

    def test_mixed_modifications(self):
        """Test with mixed modifications enabled"""
        result = dataset_label_modifier_fn(
            base_label_modifier=self.base_label,
            coerce_time=True,
            coerce_time_label=self.coerce_label,
            day_start_index_change=False,
            day_start_time_label=self.day_start_label,
            erase_meal_overlap=True,
            erase_meal_label=self.erase_meal_label
        )
        self.assertEqual(result, "_base_timeInter5mins_minCarb10g")

    def test_empty_base_label(self):
        """Test with empty base label"""
        result = dataset_label_modifier_fn(
            base_label_modifier="",
            coerce_time=True,
            coerce_time_label=self.coerce_label,
            day_start_index_change=True,
            day_start_time_label=self.day_start_label,
            erase_meal_overlap=True,
            erase_meal_label=self.erase_meal_label
        )
        self.assertEqual(result, "_timeInter5mins_dayStart4hrs_minCarb10g")