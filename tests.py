import unittest
from unittest.mock import patch, Mock, MagicMock, PropertyMock

from create_small_multiples import *


class UnitTests(unittest.TestCase):
    def test_create_chart_set__given_small_run__then_no_exceptions(self):
        # Arrange

        # Act
        METRICS = ["positiveIncrease"]  # , "hospitalizedIncrease", "deathIncrease"]
        IMAGE_SIZES = ["regular"]  # , "large"]
        specific_states = [
            "NY",
            "CA",
            "FL",
            "AZ",
            "NC",
            "MT",
            "AR",
            "WI",
            "IL",
            "VA",
            "MD",
            "DC",
        ]

        create_chart_set(
            "per_capita",
            METRICS,
            IMAGE_SIZES,
            sorted(specific_states),
        )

        # Assert

    def test_create_chart_set__given_small_run__then_no_exceptions(self):
        # Arrange

        # Act
        METRICS = ["positiveIncrease"]  # , "hospitalizedIncrease", "deathIncrease"]
        IMAGE_SIZES = ["regular"]  # , "large"]
        specific_states = [
            "NY",
            "CA",
            "FL",
            "AZ",
            "NC",
            "MT",
            "AR",
            "WI",
            "IL",
            "VA",
            "MD",
            "DC",
        ]

        create_chart_set(
            "totals",
            METRICS,
            IMAGE_SIZES,
        )

        # Assert


if __name__ == "__main__":
    unittest.main()
