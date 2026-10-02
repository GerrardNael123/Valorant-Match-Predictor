import pandas as pd

def load_and_prepare(path="data/matches.csv"):
    df = pd.read_csv(path)

    # feature turunan
    df["kd_ratio"] = df["kills"] / df["deaths"].replace(0, 1)
    df["headshot_rate"] = df["headshots"] / (
        df["headshots"] + df["bodyshots"] + df["legshots"]
    ).replace(0, 1)

    # one-hot encoding untuk map dan agent
    df = pd.get_dummies(df, columns=["map", "agent"], drop_first=True)

    df["won"] = df["won"].astype(int)
    return df

if __name__ == "__main__":
    df = load_and_prepare()
    print(df.head())
    print(df.shape)