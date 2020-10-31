import unittest
from unittest.mock import patch, Mock, MagicMock, PropertyMock

from validate_csv import *


class FileQAUnitTests(unittest.TestCase):
    def test_CSV__given_single_column_table_that_matches_expected_exactly__then_no_errors_returned(
        self,
    ):
        # Arrange
        filename = "tests/data/test_single_column.csv"
        fields = ["cola"]
        field_stats = [
            FieldStats(name="cola", delta_threshold=0.1, average=5, std_dev=3.32)
        ]

        # Act
        results = validate_csv(filename, fields, field_stats)
        print(results)

        # Assert
        self.assertEqual(len(results), 0)

    def test_CSV__given_single_column_table_avg_is_lower_outside_threshold__then_average_error_returned(
        self,
    ):
        # Arrange
        filename = "tests/data/test_single_column.csv"
        fields = ["cola"]
        field_stats = [
            FieldStats(name="cola", delta_threshold=0.1, average=4, std_dev=3.32)
        ]

        # Act
        results = validate_csv(filename, fields, field_stats)
        print(results)

        # Assert
        self.assertEqual(results, ["cola.average of 5.0 is not similar to 4"])

    def test_CSV__given_single_column_table_avg_is_higher_outside_threshold__then_average_error_returned(
        self,
    ):
        # Arrange
        filename = "tests/data/test_single_column.csv"
        fields = ["cola"]
        field_stats = [
            FieldStats(name="cola", delta_threshold=0.1, average=6, std_dev=3.32)
        ]

        # Act
        results = validate_csv(filename, fields, field_stats)
        print(results)

        # Assert
        self.assertEqual(results, ["cola.average of 5.0 is not similar to 6"])

    def test_CSV__given_single_column_table_stddev_is_outside_threshold__then_average_error_returned(
        self,
    ):
        # Arrange
        filename = "tests/data/test_single_column.csv"
        fields = ["cola"]
        field_stats = [
            FieldStats(name="cola", delta_threshold=0.1, average=5, std_dev=2.8)
        ]

        # Act
        results = validate_csv(filename, fields, field_stats)
        print(results)

        # Assert
        self.assertEqual(results, ["cola.std_dev of 3.32 is not similar to 2.8"])

    def test_CSV__given_mutli_column_table_that_matches_expected_exactly__then_no_errors_returned(
        self,
    ):
        # Arrange
        filename = "tests/data/test_multi_column.csv"
        fields = ["cola"]
        field_stats = [
            FieldStats(
                name="cola",
                delta_threshold=0.1,
                average=5,
                std_dev=3.32,
            ),
            FieldStats(
                name="colb",
                delta_threshold=0.1,
                average=83.67,
                std_dev=20.93,
            ),
        ]

        # Act
        results = validate_csv(filename, fields, field_stats)
        print(results)

        # Assert
        self.assertEqual(len(results), 0)


if __name__ == "__main__":
    unittest.main()