import pandas as pd

print("cleaning irregular data ...")
data = pd.read_csv("./caseData.csv", parse_dates=["date"], index_col="date")

for i, indice in enumerate(data.index):
    data.at[indice, "total"] = data.at[indice, "new"] + data.iloc[0:i]["new"].sum()
    data.at[indice, "recovered"] = data.at[indice, "total"] - data.at[indice, "active"] - data.iloc[0:i + 1]["dead"].sum()
    data.at[indice, "average"] = data.iloc[max([i - 6, 0]):i + 1]["new"].sum() / 7

print("cleaning complete; caseData.csv written")
data.to_csv("caseData.csv")
