import io, requests, random, time
import pandas as pd
import numpy as np
from PyPDF2 import PdfFileReader

# initialise
data = pd.read_csv("./vaxData.csv", parse_dates=["updated"], index_col="area")
vaxDate = data.updated[0] + pd.Timedelta(days=1)

# scrape vax data
print(f"checking {vaxDate:%B %-d, %Y} ...")
url = f"https://www.health.gov.au/sites/default/files/documents/{vaxDate:%Y}/{vaxDate:%m}/covid-19-vaccine-rollout-update-{vaxDate:%-d-%B-%Y}.pdf".lower()
try:
    request = requests.get(url)
    file = io.BytesIO(request.content)
    reader = PdfFileReader(file)
    contents = reader.getPage(5).extractText().split("\n")
    first = []
    second = []
    for i in range(1, 10):
        first.append(
            float(contents[contents.index("dose 1") + i].strip().replace(",", "")) +
            float(contents[len(contents) - 1 - contents[::-1].index("dose 1") + i].strip().replace(",", ""))
        )
        second.append(
            float(contents[contents.index("dose 2") + i].strip().replace(",", "")) +
            float(contents[len(contents) - 1 - contents[::-1].index("dose 2") + i].strip().replace(",", ""))
        )
    data["first"] = first
    data["second"] = second
    data["updated"] = vaxDate
except:
    print("no data available")

data.to_csv("vaxData.csv")
