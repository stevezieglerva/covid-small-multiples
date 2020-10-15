import pandas as pd
import xlrd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta

GRAY = "#808080"
RED = "#FF0000"
GREEN = "#008000"


def create_chart_set(use_per_capita, metrics, image_sizes, specific_states=[]):
    covid_data_raw = pd.read_csv("all-states-history.csv")
    print(covid_data_raw)

    population = pd.read_csv("state_2010_populations.csv")

    covid_data_raw["real_date"] = pd.to_datetime(
        covid_data_raw["date"], format="%Y-%m-%d"
    )

    covid_with_population = pd.merge(covid_data_raw, population, on="state")
    print(covid_with_population)

    state_list = covid_with_population["state"].unique()

    max_date = covid_with_population["real_date"].max()
    print(f"max_date: {max_date}")
    ninety_days_ago = max_date - timedelta(90)
    print(f"ninety_days_ago: {ninety_days_ago}")
    week_ago = max_date - timedelta(7)
    print(f"week_ago: {week_ago}")

    for metric in metrics:
        if use_per_capita == "per_capita":
            covid_with_population["reporting_field"] = (
                covid_with_population[metric] / covid_with_population["millions"]
            )
        else:
            covid_with_population["reporting_field"] = covid_with_population[metric]

        covid_cleaned_infinity_fields = covid_with_population.replace(
            [np.inf, -np.inf], np.nan
        ).dropna(subset=["reporting_field"], how="all")

        largest_states = get_largest_states(covid_cleaned_infinity_fields, week_ago)
        smallest_states = get_smallest_states(covid_cleaned_infinity_fields, week_ago)

        for earliest_date in [ninety_days_ago, datetime(2010, 5, 3)]:
            final_data = covid_cleaned_infinity_fields
            plt.subplots_adjust(hspace=0.1)
            width = 4
            height = 13
            if specific_states:
                width = 4
                height = int((len(specific_states) + 1) / width)

            max_per_capita_value = get_max_per_capita_value_for_timeframe(
                covid_cleaned_infinity_fields, earliest_date
            )

            chart_meta = f"""

_____________________________________________
metric:               {metric}
earliest_date:        {earliest_date}
height x width:       {height} x {width}
max_per_capita_value: {max_per_capita_value}
largest_states:       {largest_states}
smallest_status:      {smallest_states}

"""
            print(chart_meta)

            for image_size in image_sizes:

                current_fig_size = (10, 12)
                if image_size == "large":
                    current_fig_size = (14, 18)
                if specific_states:
                    current_fig_size = (10, 3)
                fig, ax = plt.subplots(height, width, figsize=current_fig_size)
                fig.tight_layout()
                if specific_states:
                    state_list = specific_states
                for index, state in enumerate(state_list):
                    row = int(index / width)
                    col = index % width
                    print(f"{row}, {col}. {state}")
                    state_daily = final_data[
                        (final_data["state"] == state)
                        & (final_data["real_date"] > earliest_date)
                    ][["date", metric, "reporting_field", "millions"]].sort_values(
                        "date"
                    )

                    color = get_line_color(state, largest_states, smallest_states)
                    title_annotation = get_title_annotation(
                        state, largest_states, smallest_states
                    )
                    if state in largest_states:
                        color = RED
                        title_annotation = " !"
                    if state in smallest_states:
                        color = GREEN
                        title_annotation = " *"

                    ax[row, col].plot(
                        state_daily["date"],
                        state_daily["reporting_field"].rolling(7).mean(),
                        color=color,
                    )
                    ax[row, col].set_ylim(0, max_per_capita_value)
                    ax[row, col].get_xaxis().set_visible(False)
                    ax[row, col].get_yaxis().set_visible(False)
                    ax[row, col].set_title(f"{state}{title_annotation}", y=0.9)
                if not specific_states:
                    ax[12, 3].get_xaxis().set_visible(False)
                    ax[12, 3].get_yaxis().set_visible(False)

                date_desc = "all_time"
                if earliest_date == ninety_days_ago:
                    date_desc = "90days"
                state_desc = "all_states"
                if specific_states:
                    state_desc = "specific_states"

                name = f"covid/{state_desc}/{use_per_capita}/{date_desc}/{metric}_{image_size}.png"
                fig.text(0, 0, name, fontsize=10)
                plt.savefig(name)


def get_largest_states(df, date):
    last_week_largest = (
        df[df["real_date"] >= date][["date", "state", "reporting_field"]]
        .groupby(by="state")
        .sum()
        .nlargest(3, "reporting_field")
    )
    print("Largest:")
    print(last_week_largest)
    largest_states = last_week_largest.index.values.tolist()
    print(f"largest_states: {largest_states}")
    return largest_states


def get_smallest_states(df, date):
    last_week_smallest = (
        df[df["real_date"] >= date][["date", "state", "reporting_field"]]
        .groupby(by="state")
        .sum()
        .nsmallest(3, "reporting_field")
    )
    print("Smallest:")
    print(last_week_smallest)
    smallest_states = last_week_smallest.index.values.tolist()
    print(f"smallest_states: {smallest_states}")
    return smallest_states


def get_max_per_capita_value_for_timeframe(df, earliest_date):
    max_per_capita_value = (
        df[df["real_date"] >= earliest_date]["reporting_field"].rolling(7).mean().max()
        * 1.05
    )
    return max_per_capita_value


def get_line_color(state, largest_states, smallest_states):
    color = GRAY
    if state in largest_states:
        color = RED
    if state in smallest_states:
        color = GREEN
    return color


def get_title_annotation(state, largest_states, smallest_states):
    title_annotation = ""
    if state in largest_states:
        title_annotation = " !"
    if state in smallest_states:
        title_annotation = " *"
    return title_annotation


if __name__ == "__main__":

    METRICS = ["positiveIncrease", "hospitalizedIncrease", "deathIncrease"]
    IMAGE_SIZES = ["regular", "large"]
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
        True,
        METRICS,
        IMAGE_SIZES,
        sorted(specific_states),
    )
    create_chart_set(
        False,
        METRICS,
        IMAGE_SIZES,
        sorted(specific_states),
    )
    create_chart_set(True, METRICS, IMAGE_SIZES)
    create_chart_set(False, METRICS, IMAGE_SIZES)
