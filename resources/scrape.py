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
chrome_options.add_argument("start-maximized");
chrome_options.add_argument("--headless")

# set up the browser
driver = webdriver.Chrome(options=chrome_options)

# navigate to data table
driver.get("https://www.covid19.act.gov.au/")
data_card = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CLASS_NAME, "spf-article-card--tabular"))
)

# extract values
data_table = data_card.find_element_by_class_name("spf-article-card--tabular-table")
active = data_card.find_element_by_css_selector("table td:nth-child(2)").get_attribute("innerText").replace(" Active", "")
confirmed = data_card.find_element_by_css_selector("table td:last-child").get_attribute("innerText").replace(" Total", "")
recovered = data_table.find_element_by_css_selector(".col-lg-6:nth-child(3) table td:last-child").get_attribute("innerText")
deaths = "3"
date = data_card.find_element_by_css_selector("p").get_attribute("innerText")[-10:]
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
