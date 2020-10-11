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
    for state in state_list:  # ["NC", "VA"]:
        print(state)
        state_daily = final_data[final_data["state"] == state][
            ["date", "per_capita"]
        ].sort_values("date")

        fig, ax = plt.subplots(1, 3, figsize=(1.5, 1))
        ax[0].plot(
            state_daily["date"],
            state_daily["per_capita"].rolling(7).mean(),
        )

        ax[0].set_ylim(0, max_per_capita_value)
        ax[0].get_xaxis().set_visible(False)
        ax[0].get_yaxis().set_visible(False)
        ax[0].set_title(state)
        plt.savefig(f"state_{state}.png", bbox_inches="tight")

        # Create figure and plot space


if __name__ == "__main__":
    main()
