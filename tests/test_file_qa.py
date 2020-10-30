import unittest
from unittest.mock import patch, Mock, MagicMock, PropertyMock

from validate_csv import *


class FileQAUnitTests(unittest.TestCase):
    def test_CSV__given_simple_data_that_is_valid__then_no_errors_returned(self):
        # Arrange
        filename = "filename.csv"
        fields = ["cola", "colb"]
        field_stats = [
            FieldStats(
                name="cola", delta_threshold=0.1, min=1, max=20, average=10, std_dev=2
            )
        ]

        # Act
        results = validate_csv(filename, fields, field_stats)

        # Assert


if __name__ == "__main__":
    unittest.main()