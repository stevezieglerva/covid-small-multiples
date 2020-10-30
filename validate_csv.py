import pandas
import collections

FieldStats = collections.namedtuple(
    "FieldStats", "name delta_threshold average std_dev min max"
)


def validate_csv(filename, fields, field_stats=[]):
    pass