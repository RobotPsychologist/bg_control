from meal_identification.datasets.dataset_operations import get_root_dir
import unittest
import os
import shutil
import tempfile


class TestGetRootDir(unittest.TestCase):
    def setUp(self):
        """Create a temporary directory structure for testing."""
        # Create a temp root for testing
        self.temp_root = tempfile.mkdtemp()

        # Create the .github directory in the root
        self.github_dir = os.path.join(self.temp_root, '.github')
        os.makedirs(self.github_dir)

        # Create some nested dirs
        self.nested_dirs = [
            os.path.join(self.temp_root, '0_meal_identification'),
            os.path.join(self.temp_root, '0_meal_identification', 'meal_identification'),
            os.path.join(self.temp_root, '0_meal_identification', 'meal_identification', 'datasets')
        ]

        for dir_path in self.nested_dirs:
            os.makedirs(dir_path)

    def tearDown(self):
        """Clean up the temporary directory structure."""
        shutil.rmtree(self.temp_root)

    def test_find_root_from_root_dir(self):
        """Test finding root directory from root."""
        result = get_root_dir(self.temp_root)
        self.assertEqual(result, self.temp_root)

    def test_find_root_from_nested_dir(self):
        """Test finding root directory from a nested directory."""
        for dir_path in self.nested_dirs:
            result = get_root_dir(dir_path)
            self.assertEqual(result, self.temp_root)

    def test_no_github_dir(self):
        """Test that function raises FileNotFoundError when no .github directory not found."""
        # Create a separate directory structure without .github
        temp_dir = tempfile.mkdtemp()
        try:
            with self.assertRaises(FileNotFoundError):
                get_root_dir(temp_dir)
        finally:
            shutil.rmtree(temp_dir)

    def test_none_current_dir(self):
        """Test that function works when current_dir is None."""
        original_cwd = os.getcwd()
        try:
            os.chdir(self.nested_dirs[0])
            # In Mac OS X, /var is a symlink to /private/var.
            result = get_root_dir()
            expected = os.path.realpath(self.temp_root)
            self.assertEqual(result, expected)
        finally:
            os.chdir(original_cwd)