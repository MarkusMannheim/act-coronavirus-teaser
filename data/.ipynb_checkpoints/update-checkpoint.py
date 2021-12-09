import io, requests
import pandas as pd, numpy as np
from PyPDF2 import PdfFileReader

def vaxScrape(date):
    print()
    print(f"checking vaccination data for {date:%B %-d, %Y} ...")
    url = f"https://www.health.gov.au/sites/default/files/documents/{date:%Y}/{date:%m}/covid-19-vaccine-rollout-update-{date:%-d-%B-%Y}.pdf".lower()

    try:
        request = requests.get(url)
        file = io.BytesIO(request.content)
        reader = PdfFileReader(file)
        contents = reader.getPage(5).extractText().split("\n")

        for i in range(9):
            try:
                first_16 = float(contents[contents.index("dose 1") + i + 1].strip().replace(",", ""))
                first_12 = float(contents[len(contents) - contents[::-1].index("dose 1") + i].strip().replace(",", ""))
                second_16 = float(contents[contents.index("dose 2") + i + 1].strip().replace(",", ""))
                second_12 = float(contents[len(contents) - contents[::-1].index("dose 2") + i].strip().replace(",", ""))

            except:
                first_16 = float(contents[contents.index("-dose 1") + i + 1].strip().replace(",", ""))
                first_12 = float(contents[len(contents) - contents[::-1].index("-dose 1") + i].strip().replace(",", ""))
                second_16 = float(contents[contents.index("-dose 2") + i + 1].strip().replace(",", ""))
                second_12 = float(contents[len(contents) - contents[::-1].index("-dose 2") + i].strip().replace(",", ""))

            vaxData.iloc[i] = [first_16 + first_12, second_16 + second_12]

        vaxData["population"] = [25704340, 431826, 8176368, 247023, 5206400, 1771703, 541965, 6648564, 2675797]
        vaxData["first_percent"] = vaxData["first"] / vaxData["population"]
        vaxData["second_percent"] = vaxData["second"] / vaxData["population"]
        vaxData.sort_values("second_percent", ascending=True, inplace=True)
        vaxData["date"] = date
        vaxData.to_csv("vaxData.csv")
        print(f"data found; vaxData.csv written")

    except:
        print(f"data unavailable for this date")
        date = date - pd.Timedelta(days=1)
        vaxScrape(date)

def caseScrape(date):
    print()
    print(f"Input case data for {date:%A, %B %-d, %Y}:")
    data.at[date, "new"] = float(input("New cases: "))
    data.at[date, "active"] = float(input("Active cases: "))
    data.at[date, "hospitalised"] = float(input("In hospital: "))
    data.at[date, "intensive care"] = float(input("In intensive care: "))
    data.at[date, "ventilated"] = float(input("On ventilation: "))
    data.at[date, "dead"] = float(input("Deaths in past day: "))
    data.at[date, "tests"] = float(input("Negative tests returned: "))

    if today > date:
        date = date + pd.Timedelta(days=1)
        if today == date:
            todayCase(date)
        else:
            caseScrape(date)

def todayCase(date):
    print()
    ready = input("Are today's case data available yet? (Y/N) ")
    if ready.lower() == "y":
        caseScrape(date)
    else:
        print("Remember to check later today.")

def clean():
    print()
    print("cleaning irregular data ...")
    for i, indice in enumerate(data.index):
        data.at[indice, "total"] = data.at[indice, "new"] + data.iloc[0:i]["new"].sum()
        data.at[indice, "recovered"] = data.at[indice, "total"] - data.at[indice, "active"] - data.iloc[0:i + 1]["dead"].sum()
        data.at[indice, "average"] = data.iloc[max([i - 6, 0]):i + 1]["new"].sum() / 7
    print("cleaning complete; caseData.csv written")
    data.to_csv("caseData.csv")

# CASE DATA
print("checking existing case data ...")
data = pd.read_csv("./caseData.csv", parse_dates=["date"], index_col="date")
lastDate = data.index[-1] + pd.Timedelta(days=1)
today = pd.to_datetime(pd.Timestamp("now").date())

if today < lastDate:
    print("case data is up-to-date")
elif today == lastDate:
    todayCase(lastDate)
else:
    caseScrape(lastDate)
clean()

# VACCINATION DATA
vaxData = pd.DataFrame(
    index=["AUS", "ACT", "NSW", "NT", "QLD", "SA", "TAS", "VIC", "WA"],
    columns=["first", "second"]
)
vaxData.index.name = "jurisdiction"

date = pd.Timestamp("now").date()
vaxScrape(date)
