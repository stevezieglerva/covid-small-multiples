import pandas as pd
import xlrd
import matplotlib.pyplot as plt


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

    state_list = covid_with_population["state"].unique()
    print(state_list)

    for state in ["NC", "VA", "NY", "FL", "CA"]:
        state_daily = covid_with_population[covid_with_population["state"] == state][
            ["date", "per_capita"]
        ].sort_values("date")

        fig, ax = plt.subplots(figsize=(4, 4))
        ax.plot(state_daily["date"], state_daily["per_capita"].rolling(7).mean())

        plt.savefig(f"{state}.png")

        # Create figure and plot space


if __name__ == "__main__":
    main()
