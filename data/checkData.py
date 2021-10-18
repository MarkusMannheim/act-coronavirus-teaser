import io, requests, random
import pandas as pd, numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PyPDF2 import PdfFileReader

def vaxScrape(date):
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
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=chrome_options)

    print(f"scraping ACT cases for {date:%B %-d, %Y} ...")
    driver.get(f"https://www.covid19.act.gov.au/news-articles/act-covid-19-update-{date:%-d-%B-%Y}".lower())

    try:
        outcomes = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".ultra-condensed td p"))
        )
        outcomes = [outcome.get_attribute("innerText") for outcome in outcomes if outcome.get_attribute("innerText") != ""]
        data.at[date, "new"] = float(outcomes[2])
        data.at[date, "active"] = float(outcomes[4])
        data.at[date, "hospitalised"] = float(outcomes[8])
        data.at[date, "intensive care"] = float(outcomes[10])
        data.at[date, "dead"] = data["dead"].sum() - float(outcomes[12])
        print("data found and recorded")

    except:
        print("no data found")

    if today > date:
        lastDate = date + pd.Timedelta(days=1)
        caseScrape(lastDate)

    else:
        driver.close()
        driver.quit()
        for i, indice in enumerate(data.index):
            data.at[indice, "total"] = data.at[indice, "new"] + data.iloc[0:i]["new"].sum()
            data.at[indice, "recovered"] = data.at[indice, "total"] - data.at[indice, "active"] - data.iloc[0:i + 1]["dead"].sum()
            data.at[indice, "average"] = data.iloc[max([i - 6, 0]):i + 1]["new"].sum() / 7
        print("case data check complete; caseData.csv written")
        data.to_csv("caseData.csv")

# CASE DATA

print("checking existing case data ...")
data = pd.read_csv("./caseData.csv", parse_dates=["date"], index_col="date")
lastDate = data.index[-1]

today = pd.to_datetime(pd.Timestamp("now").date())
if today <= lastDate:
    print("case data is up-to-date")
else:
    caseScrape(lastDate)

# VACCINATION DATA

vaxData = pd.DataFrame(
    index=["AUS", "ACT", "NSW", "NT", "QLD", "SA", "TAS", "VIC", "WA"],
    columns=["first", "second"]
)
vaxData.index.name = "jurisdiction"

date = pd.Timestamp("now").date()
vaxScrape(date)
