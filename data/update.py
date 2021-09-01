import io, requests
import pandas as pd, numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PyPDF2 import PdfFileReader

# load dataset
print("checking existing data ...")
data = pd.read_csv("./data.csv", parse_dates=["date"], index_col="date")
last_date = data.index[-1]

# use a headless browser (saves time)
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=chrome_options)

# scrape ACT data
print("scraping ACT website ...")
driver.get("https://www.covid19.act.gov.au/updates/act-covid-19-statistics")
date = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, ".spf-article-card--tabular-subtitle p"))
)
date = pd.to_datetime(date.get_attribute("innerText").split(", ")[1])
stats = driver.find_elements_by_class_name("stat-card-number")
new = float(stats[0].get_attribute("innerText"))
active = float(stats[1].get_attribute("innerText"))

driver.close()
driver.quit()

# fill new data
print(f"latest data for {date:%B %-d, %Y}:")
data.at[date, "new"] = new
print(f"{new:,.0f} new cases")
data.at[date, "total"] = data.at[date - pd.Timedelta(days=1), "total"] + new
print(f"{data.at[date, 'total']:,.0f} new cases")
data.at[date, "dead"] = data.at[date - pd.Timedelta(days=1), "dead"]
print(f"{data.at[date, 'dead']:,.0f} dead")
data.at[date, "recovered"] = data.at[date, "total"] - data.at[date, "dead"] - active
print(f"{data.at[date, 'recovered']:,.0f} recovered")

# scrape missing vax data
vaxDate = date
while True:
    if (data.at[vaxDate, "first"] == 0) or (np.isnan(data.at[vaxDate, "first"])):
        print("scraping vaccination reports ...")
        print(f"checking {vaxDate:%B %-d, %Y} ...")
        url = f"https://www.health.gov.au/sites/default/files/documents/{vaxDate:%Y}/{vaxDate:%m}/covid-19-vaccine-rollout-update-{vaxDate:%-d-%B-%Y}.pdf".lower()
        try:
            request = requests.get(url)
            file = io.BytesIO(request.content)
            reader = PdfFileReader(file)
            contents = reader.getPage(5).extractText().split("\n")
            first = float(contents[contents.index("dose 1") + 2].strip().replace(",", ""))
            second = float(contents[contents.index("dose 2") + 2].strip().replace(",", ""))
            data.at[vaxDate, "first"] = first
            data.at[vaxDate, "second"] = second
            vaxDate = vaxDate - pd.Timedelta(days=1)
        except:
            print("no data available")
            vaxDate = vaxDate - pd.Timedelta(days=1)
    else:
        break

# fill in calculated fields
print("calculating remaining fields ...")
data["half"] = (data["first"] - data["second"]) / 344014
data["full"] = data["second"] / 344014
for i, date in enumerate(data.index):
    data.at[date, "average"] = data.iloc[max(i - 6, 0):i + 1]["new"].mean()
data.to_csv("data.csv", index_label="date")
print("date.csv written")
