import io, requests, time
import pandas as pd, numpy as np, matplotlib.pyplot as plt, seaborn as sns
from PyPDF2 import PdfFileReader
sns.set(font_scale=1.5, style="whitegrid")

vaxData = pd.DataFrame(
    index=["AUS", "ACT", "NSW", "NT", "QLD", "SA", "TAS", "VIC", "WA"],
    columns=["first", "second"]
)
vaxData.index.name = "jurisdiction"

date = pd.Timestamp("now").date()
print(f"checking {date:%B %-d, %Y} ...")
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

except:
    print(f"data not yet ready for today")

vaxData.to_csv("vaxData.csv")
