import pandas as pd
import xlrd
import matplotlib.pyplot as plt


def main():
    df = pd.read_csv("all-states-history.csv")
    print(df)

    state_list = df["state"].unique()
    print(state_list)

    for state in ["NC", "VA"]:
        state_daily = df[df["state"] == state][
            ["date", "positiveIncrease"]
        ].sort_values("date")

        print(state_daily)
        fig, ax = plt.subplots(figsize=(4, 4))
        ax.plot(state_daily["date"], state_daily["positiveIncrease"].rolling(7).mean())

        plt.savefig(f"{state}.png")

        # Create figure and plot space


if __name__ == "__main__":
    main()
