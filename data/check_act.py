# modules
import pandas as pd
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# use a headless browser (saves time)
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=chrome_options)

# scrape ACT Health data
print("checking ACT Health website ...")
driver.get(f"https://www.covid19.act.gov.au/updates/act-covid-19-statistics?randomKey={random.randint(1000, 9999)}")
lastDate = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, ".spf-article-card--tabular-subtitle p"))
)
lastDate = lastDate.get_attribute("innerText").strip()
lastDate = pd.to_datetime(lastDate[lastDate.index(",") + 2:], format="%d %b %Y")

activeCases = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.CLASS_NAME, "stat-card-number"))
)
activeCases = float(activeCases.get_attribute("innerText"))

driver.close()
driver.quit()
   
data = pd.read_csv("./case_data.csv")
data["date"] = pd.to_datetime(data["date"], format="%Y/%m/%d")
data.sort_values("date", ascending=True, inplace=True)
data.fillna(0, inplace=True)
data["new"] = data["new"].astype("float")
data["total"] = data["total"].astype("float")

lastRow = len(data) - 1

if lastDate > data.at[lastRow, "date"]:
    print("new ACT data found:")
    data.loc[lastRow + 1] = [
        lastDate,
        activeCases - data.at[lastRow, "new"],
        data.at[lastRow, "total"] + activeCases - data.at[lastRow, "new"],
        data.at[lastRow, "recovered"] + data.at[lastRow, "new"] - activeCases,
        data.at[lastRow, "dead"],
        None,
        None
    ]
    print(data.loc[lastRow + 1])
    data.to_csv("./case_data.csv", index=False)
    print("case_data.csv written")
    data["one"] = (data["first"] - data["second"]) / 344013
    data["two"] = data["second"] / 344013
    data = data[list(data.columns)[:5] + list(data.columns)[-2:]]
    data.at[lastRow, "average"] = data.iloc[lastRow - 6:]["new"].mean()
    data.to_csv("./data.csv", index=False)
    print("data.csv written")
else:
    print("no update found")
    print(f"last date was {lastDate:%b %d, %Y}")