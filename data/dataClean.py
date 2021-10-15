import pandas as pd

data = pd.read_csv(
    "caseData.csv",
    parse_dates=["date"],
    index_col="date"
)
