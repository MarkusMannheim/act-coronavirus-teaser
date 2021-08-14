# modules
import pandas as pd
import io, requests
from PyPDF2 import PdfFileReader

# load data, check date
data = pd.read_csv("./case_data.csv")
data["date"] = pd.to_datetime(data["date"], format="%Y/%m/%d")
data.sort_values("date", ascending=True, inplace=True)
data.fillna(0, inplace=True)
data["new"] = data["new"].astype("float")
data["total"] = data["total"].astype("float")
lastRow = len(data) - 1
lastDate = data.at[lastRow, "date"]

# data collected for latest date?
if data.at[lastRow, "first"] > 0:
    print(f"federal data already collected for {lastDate:%b %d, %Y}")
else:
    # scrape federal data
    print("checking federal Health Department website ...")
    url = f"https://www.health.gov.au/sites/default/files/documents/2021/08/covid-19-vaccine-rollout-update-{lastDate:%d-%B-%Y}.pdf".lower()
    try:
        request = requests.get(url)
        file = io.BytesIO(request.content)
        reader = PdfFileReader(file)
        contents = reader.getPage(2).extractText().split("\n")
        print("update found")
        first = contents[contents.index("dose 1") + 2]
        second = contents[contents.index("dose 2") + 2]
        print(f"one-plus doses: {first}; two doses: {second}")
        data.at[lastRow, "first"] = float(first.replace(",", ""))
        data.at[lastRow, "second"] = float(second.replace(",", ""))
        data.to_csv("./case_data.csv", index=False)
        print("case_data.csv written")
        data["one"] = (data["first"] - data["second"]) / 344013
        data["two"] = data["second"] / 344013
        data = data[list(data.columns)[:5] + list(data.columns)[-2:]]
        data.at[lastRow, "average"] = data.iloc[lastRow - 6:]["new"].mean()
        data.to_csv("./data.csv", index=False)
        print("data.csv written")
    except:
        print("no data available yet")
        lastDate = data.at[lastRow - 1, "date"]
        print(f"last date was {lastDate:%b %d, %Y}")
