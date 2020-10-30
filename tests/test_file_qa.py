import unittest
from unittest.mock import patch, Mock, MagicMock, PropertyMock

from validate_csv import *


class FileQAUnitTests(unittest.TestCase):
    def test_CSV__given_simple_data_that_is_valid__then_no_errors_returned(self):
        # Arrange
        filename = "filename.csv"
        fields = ["cola", "colb"]

        # Act
        results = validate_csv(filename, fields)

        # Assert


if __name__ == "__main__":
    unittest.main()