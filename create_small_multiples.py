import pandas as pd
import xlrd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta

GRAY = "#808080"
RED = "#FF0000"
GREEN = "#008000"

METRICS = ["positiveIncrease"]  # , "hospitalizedIncrease", "deathIncrease"]
IMAGE_SIZES = ["regular"]


def main():
    covid_data_raw = pd.read_csv("all-states-history.csv")
    print(covid_data_raw)

    population = pd.read_csv("state_2010_populations.csv")
    print(population)

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

    for metric in METRICS:
        covid_with_population["per_capita"] = (
            covid_with_population[metric] / covid_with_population["millions"]
        )

        covid_cleaned_infinity_fields = covid_with_population.replace(
            [np.inf, -np.inf], np.nan
        ).dropna(subset=["per_capita"], how="all")

        last_day_largest = (
            covid_cleaned_infinity_fields[
                covid_cleaned_infinity_fields["real_date"] >= week_ago
            ][["date", "state", "per_capita"]]
            .groupby(by="state")
            .sum()
            .nlargest(3, "per_capita")
        )
        print("Largest:")
        print(last_day_largest)
        largest_states = last_day_largest.index.values.tolist()
        print(f"largest_states: {largest_states}")

        last_day_smallest = (
            covid_cleaned_infinity_fields[
                covid_cleaned_infinity_fields["real_date"] >= week_ago
            ][["date", "state", "per_capita"]]
            .groupby(by="state")
            .sum()
            .nsmallest(3, "per_capita")
        )
        print("Smallest:")
        print(last_day_smallest)
        smallest_states = last_day_smallest.index.values.tolist()
        print(f"smallest_states: {smallest_states}")

        for earliest_date in [ninety_days_ago, datetime(2010, 5, 3)]:
            final_data = covid_cleaned_infinity_fields
            plt.subplots_adjust(hspace=0.1)
            width = 4
            height = 13

            max_per_capita_value = (
                covid_cleaned_infinity_fields[
                    covid_cleaned_infinity_fields["real_date"] >= earliest_date
                ]["per_capita"]
                .rolling(7)
                .mean()
                .max()
                * 1.05
            )

            for image_size in IMAGE_SIZES:
                chart_meta = f"""

_____________________________________________
metric: {metric}
earliest_date: {earliest_date}
image_size: {image_size}
max_per_capita_value: {max_per_capita_value}
"""
                print(chart_meta)

                current_fig_size = (10, 12)
                if image_size == "large":
                    current_fig_size = (14, 18)
                fig, ax = plt.subplots(height, width, figsize=current_fig_size)
                fig.tight_layout()
                for index, state in enumerate(["NC", "MT", "SC", "SD", "NY"]):
                    row = int(index / width)
                    col = index % width
                    print(f"{row}, {col}. {state}")
                    state_daily = final_data[
                        (final_data["state"] == state)
                        & (final_data["real_date"] > earliest_date)
                    ][["date", "per_capita"]].sort_values("date")

                    color = GRAY
                    title_annotation = ""
                    if state in largest_states:
                        color = RED
                        title_annotation = " !"
                    if state in smallest_states:
                        color = GREEN
                        title_annotation = " *"

                    ax[row, col].plot(
                        state_daily["date"],
                        state_daily["per_capita"].rolling(7).mean(),
                        color=color,
                    )
                    ax[row, col].set_ylim(0, max_per_capita_value)
                    ax[row, col].get_xaxis().set_visible(False)
                    ax[row, col].get_yaxis().set_visible(False)
                    ax[row, col].set_title(f"{state}{title_annotation}", y=0.9)
                ax[12, 3].get_xaxis().set_visible(False)
                ax[12, 3].get_yaxis().set_visible(False)

                date_desc = "all_time"
                if earliest_date == ninety_days_ago:
                    date_desc = "90days"
                plt.savefig(f"covid_all_states_{metric}_{date_desc}_{image_size}.png")


if __name__ == "__main__":

    main()
