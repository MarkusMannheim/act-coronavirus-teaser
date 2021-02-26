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

# navigate to data
driver.get("https://www.covid19.act.gov.au/")
driver.maximize_window()
data_card = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CLASS_NAME, "spf-article-card--tabular"))
)

# extract values
data_table = data_card.find_element_by_class_name("spf-article-card--tabular-table")
active = data_table.find_element_by_css_selector(".col-lg-4 table td:nth-child(2)").get_attribute("innerText").strip()[:-7]
confirmed = data_table.find_element_by_css_selector(".col-lg-4 table td:last-child").get_attribute("innerText").strip()[:-6]
recovered = data_table.find_element_by_css_selector(".col-lg-4:last-child table td:last-child").get_attribute("innerText").strip()
deaths = "3"
date = data_card.find_element_by_css_selector(".spf-article-card--tabular-subtitle p").get_attribute("innerText")[-10:]
date = pd.to_datetime(date, format="%d/%m/%Y")

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

driver.quit()
quit()
