from datetime import datetime, timedelta
import pandas as pd
from tabulate import tabulate
from selenium import webdriver
import warnings
from bs4 import BeautifulSoup as BSoup
from lxml import etree
import os

warnings.filterwarnings('ignore')

st.title('Upcoming Corporate Action')

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--no-sandbox")

driver = webdriver.Chrome(executable_path= os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)

driver.get("https://www.bseindia.com/corporates/corporates_act.html")
driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

soup = BSoup(driver.page_source, 'html.parser')
dom = etree.HTML(str(soup))

rows = 1 + len(dom.xpath("/html/body/div[5]/div/div/div/table[1]/tbody/tr/td/div/table/tbody/tr"))

stock=[]
ex_date=[]
purpose=[]

replace = '!?_@#$%^&*.,-'

for r in range(2, rows + 1):
    try:
        date = (dom.xpath("/html/body/div[5]/div/div/div/table[1]/tbody/tr/td/div/table/tbody/tr[" + str(r) + "]/td[3]")[0].text)

        for i in range(25):
            d = (datetime.now() + timedelta(i)).strftime("%d " "%b " "%Y")

            if(date.strip() == d):
                stock_name = (dom.xpath("/html/body/div[5]/div/div/div/table[1]/tbody/tr/td/div/table/tbody/tr[" + str(r) + "]/td[2]")[0].text)
                stock_name = stock_name.strip()
                for k in replace:
                    stock_name = stock_name.replace(k, "")

                stock.append(stock_name)
                purpose.append(dom.xpath("/html/body/div[5]/div/div/div/table[1]/tbody/tr/td/div/table/tbody/tr[" + str(r) + "]/td[4]")[0].text)
                ex_date.append(d)
    except:
        continue


driver.quit()
results = pd.DataFrame(list(zip(stock, ex_date, purpose)), columns=['Stock', 'Ex-Date', 'Purpose'])
results.index+=1
st.table(results)
