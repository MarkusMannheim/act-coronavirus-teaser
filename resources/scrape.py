import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# read in existing data
data = pd.read_csv("./actData.csv")
data["date"] = pd.to_datetime(data["date"], format="%Y-%m-%d")

# use a headless browser (saves time)
chrome_options = Options()
chrome_options.add_argument("--headless")

# set up the browser
driver = webdriver.Chrome(options=chrome_options)

# attempt to reach dashboard
driver.get("https://www.covid19.act.gov.au/")
time.sleep(10)
driver.find_element_by_css_selector(".current-status_container a").click()
# check if dashboard opens
time.sleep(5)
driver.switch_to.window(driver.window_handles[-1])
time.sleep(5)
cards = driver.find_elements_by_css_selector(".visual-card svg tspan")
# extract values
recovered = cards[0].get_attribute("textContent")
confirmed = cards[2].get_attribute("textContent")
deaths = cards[4].get_attribute("textContent")
date = cards[6].get_attribute("textContent")
date = pd.to_datetime(date, format="%d/%m/%Y")
active = cards[7].get_attribute("textContent")

# if data is new, add it to file
if date > data.iloc[-1]["date"]:
    print("New data available")
    print("date:", date)
    print("confirmed:", confirmed)
    print("recovered:", recovered)
    print("deaths:", deaths)
    print("active:", active)
    print("Saving new data to file ...")
    data.loc[len(data)] = [pd.to_datetime(date, format="%d/%m/%Y"), confirmed, recovered, deaths, active]
    data["date"] = data["date"].apply(lambda d: f"{d: %Y-%m-%d}")
    data.to_csv("actData.csv", index=False)
else:
    print("No new data available")

driver.close()
