import pandas as pd
import collections
import sys


FieldStats = collections.namedtuple(
    "FieldStats", "name delta_threshold average std_dev"
)


def validate_csv(filename, field_stats=[]):
    print("in test")
    df = pd.read_csv(filename)
    print(df)
    results = []
    for field_stat in field_stats:
        field = field_stat.name
        print(field)
        file_column_desc = df[field].describe()
        print(file_column_desc)

        expected_avg = field_stat.average
        actual_avg = round(file_column_desc["mean"], 2)
        percent_delta = round(abs((actual_avg - expected_avg)) / expected_avg, 2)
        if percent_delta > field_stat.delta_threshold:
            results.append(
                f"{field}.average of {actual_avg} is not similar to {expected_avg}"
            )

        expected_stddev = field_stat.std_dev
        actual_stddev = round(file_column_desc["std"], 2)
        percent_delta = round(
            abs((actual_stddev - expected_stddev)) / expected_stddev, 2
        )
        print(percent_delta)
        if percent_delta > field_stat.delta_threshold:
            results.append(
                f"{field}.std_dev of {actual_stddev} is not similar to {expected_stddev}"
            )
    return results