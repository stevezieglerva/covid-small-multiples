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

    metrics = ["positiveIncrease", "hospitalizedIncrease", "deathIncrease"]
    for metric in metrics:
        covid_with_population["per_capita"] = (
            covid_with_population[metric] / covid_with_population["millions"]
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
        # plt.tight_layout(pad=0, w_pad=3, h_pad=3)
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

            ax[row, col].plot(
                state_daily["date"],
                state_daily["per_capita"].rolling(7).mean(),
            )
            ax[row, col].set_ylim(0, max_per_capita_value)
            ax[row, col].get_xaxis().set_visible(False)
            ax[row, col].get_yaxis().set_visible(False)
            ax[row, col].set_title(state, y=0.9)
        ax[12, 3].get_xaxis().set_visible(False)
        ax[12, 3].get_yaxis().set_visible(False)
        plt.savefig(f"covid_all_states_{metric}.png")


if __name__ == "__main__":
    main()
