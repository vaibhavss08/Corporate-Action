from selenium import webdriver
import time
import os
import pandas as pd
from tabulate import tabulate
from datetime import datetime, timedelta
import warnings
import streamlit as st

st.title('Target')

warnings.filterwarnings('ignore')

chrome_options = webdriver.ChromeOptions()
PATH = "C:\Program Files (x86)\chromedriver.exe"
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--no-sandbox")

driver = webdriver.Chrome(executable_path= os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)

pd.set_option('display.max_colwidth', None)
driver.get("https://www.bseindia.com/corporates/corporates_act.html")
driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
time.sleep(5)

rows = 1 + len(driver.find_elements_by_xpath("/html/body/div[5]/div/div/div/table[1]/tbody/tr/td/div/table/tbody/tr"))

stock=[]
ex_date=[]
purpose=[]

for r in range(2, rows + 1):
    try:
        date = driver.find_element_by_xpath("/html/body/div[5]/div/div/div/table[1]/tbody/tr/td/div/table/tbody/tr[" + str(r) + "]/td[3]")
        for i in range(25):
            d = (datetime.now() + timedelta(i)).strftime("%d " "%b " "%Y")

            if(date.text.strip() == d):
                stock.append(driver.find_element_by_xpath(
                    "/html/body/div[5]/div/div/div/table[1]/tbody/tr/td/div/table/tbody/tr[" + str(r) + "]/td[2]").text)
                purpose.append(driver.find_element_by_xpath(
                    "/html/body/div[5]/div/div/div/table[1]/tbody/tr/td/div/table/tbody/tr[" + str(r) + "]/td[4]").text)

                ex_date.append(d)
    except:
        continue


results = pd.DataFrame(list(zip(stock, ex_date, purpose)), columns=['Stock', 'Ex-Date', 'Purpose'])
pd.set_option('display.max_colwidth', None)
results.index+=1
st.table(results)
driver.quit()