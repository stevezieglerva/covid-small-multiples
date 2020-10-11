import pandas as pd
import xlrd
import matplotlib.pyplot as plt
import numpy as np

GRAY = "#808080"
RED = "#FF0000"
GREEN = "#008000"


def main():
    covid_data_raw = pd.read_csv("all-states-history.csv")
    print(covid_data_raw)

    population = pd.read_csv("state_2010_populations.csv")
    print(population)

    covid_with_population = pd.merge(covid_data_raw, population, on="state")
    print(covid_with_population)

    max_date = covid_with_population["date"].max()
    print(f"max_date: {max_date}")

    metrics = ["positiveIncrease", "hospitalizedIncrease", "deathIncrease"]
    for metric in metrics:
        covid_with_population["per_capita"] = (
            covid_with_population[metric] / covid_with_population["millions"]
        )

        no_inf = covid_with_population.replace([np.inf, -np.inf], np.nan).dropna(
            subset=["per_capita"], how="all"
        )

        max_per_capita_value = no_inf["per_capita"].rolling(7).mean().max() * 1.05
        print(f"max_per_capita_value: {max_per_capita_value}")

        last_day_largest = no_inf[no_inf["date"] == max_date][
            ["date", "state", "per_capita"]
        ].nlargest(3, "per_capita")
        print("Largest:")
        print(last_day_largest)
        largest_states = last_day_largest["state"].tolist()

        last_day_smallest = no_inf[no_inf["date"] == max_date][
            ["date", "state", "per_capita"]
        ].nsmallest(3, "per_capita")
        print("Smallest:")
        print(last_day_smallest)
        smallest_states = last_day_smallest["state"].tolist()

        state_list = covid_with_population["state"].unique()
        print(state_list)

        final_data = no_inf
        plt.subplots_adjust(hspace=0.1)
        width = 4
        height = 13
        fig, ax = plt.subplots(height, width, figsize=(10, 12))
        fig.tight_layout()
        for index, state in enumerate(state_list):  # ["NC", "VA", "SC", "ND"]):
            row = int(index / width)
            col = index % width
            print(f"{row}, {col}. {state}")
            state_daily = final_data[final_data["state"] == state][
                ["date", "per_capita"]
            ].sort_values("date")

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
        plt.savefig(f"covid_all_states_{metric}.png")


if __name__ == "__main__":

    main()
