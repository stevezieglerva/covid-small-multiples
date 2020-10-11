import pandas as pd
import xlrd
import matplotlib.pyplot as plt
import numpy as np


def main():
    covid_data_raw = pd.read_csv("all-states-history.csv")
    print(covid_data_raw)

    population = pd.read_csv("state_2010_populations.csv")
    print(population)

    covid_with_population = pd.merge(covid_data_raw, population, on="state")
    print(covid_with_population)

    covid_with_population["per_capita"] = (
        covid_with_population["positiveIncrease"] / covid_with_population["millions"]
    )

    no_inf = covid_with_population.replace([np.inf, -np.inf], np.nan).dropna(
        subset=["per_capita"], how="all"
    )
    max_by_state = no_inf.groupby(by="state")["per_capita"].max()
    print(max_by_state)
    max_per_capita_value = no_inf["per_capita"].rolling(7).mean().max() * 1.05

    print(f"max_per_capita_value: {max_per_capita_value}")

    state_list = covid_with_population["state"].unique()
    print(state_list)

    final_data = no_inf
    width = 4
    height = 13
    fig, ax = plt.subplots(height, width, figsize=(10, 10))
    for index, state in enumerate(state_list):  # ["NC", "VA", "SC", "ND"]):
        row = int(index / width)
        col = index % width
        print(f"{row}, {col}. {state}")
        state_daily = final_data[final_data["state"] == state][
            ["date", "per_capita"]
        ].sort_values("date")

        ax[row, col].plot(
            state_daily["date"],
            state_daily["per_capita"].rolling(7).mean(),
        )

        ax[row, col].set_ylim(0, max_per_capita_value)
        ax[row, col].get_xaxis().set_visible(False)
        ax[row, col].get_yaxis().set_visible(False)
        ax[row, col].set_title(state)
    plt.savefig(f"all_states.png")

    # Create figure and plot space


if __name__ == "__main__":
    main()
