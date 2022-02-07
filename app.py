from datetime import datetime, timedelta
import pandas as pd
from tabulate import tabulate
from selenium import webdriver
import warnings
import streamlit as st
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
result = []

replace = '!?_@#$%^*.,-'

flag = False

for r in range(2, rows + 1):
    try:
        date = (dom.xpath("/html/body/div[5]/div/div/div/table[1]/tbody/tr/td/div/table/tbody/tr[" + str(r) + "]/td[3]")[0].text)

        if flag or datetime.now().strftime("%d/%m/%Y") <= datetime.strptime(date,"%d %b %Y").strftime("%d/%m/%Y"):
            stock_name = (dom.xpath(
                "/html/body/div[5]/div/div/div/table[1]/tbody/tr/td/div/table/tbody/tr[" + str(r) + "]/td[2]")[0].text)
            stock_name = stock_name.strip()
            for k in replace:
                stock_name = stock_name.replace(k, "")

            stock.append(stock_name)
            purpose.append(dom.xpath(
                "/html/body/div[5]/div/div/div/table[1]/tbody/tr/td/div/table/tbody/tr[" + str(r) + "]/td[4]")[0].text)
            ex_date.append(date)
            flag = True
        else:
            continue
    except:
        continue


driver.get("https://www.bseindia.com/corporates/Forth_Results.html")

soup = BSoup(driver.page_source, 'html.parser')
dom = etree.HTML(str(soup))

rows = 1 + len(dom.xpath("/html/body/div[5]/div/div/div/table/tbody/tr/td/table/tbody/tr"))
flag = True
stock_result= []
result_date = []


for r in range(2, rows):
   stock_result.append(dom.xpath("/html/body/div[5]/div/div/div/table/tbody/tr/td/table/tbody/tr["+str(r)+"]/td[2]")[0].text)
   result_date.append(dom.xpath("/html/body/div[5]/div/div/div/table/tbody/tr/td/table/tbody/tr["+str(r)+"]/td[3]")[0].text)


results = pd.DataFrame(list(zip(stock, ex_date, purpose)), columns=['Stock', 'Ex-Date', 'Purpose'])

list = pd.read_csv("bse.csv", encoding='latin-1')

id = []

for i in stock:
    cond = list['Security Name'] == i
    id.append(list['Security Id'].loc[cond].str.cat(sep='\n'))

stock_re = []

for i in id:
    try:
        stock_re.append(result_date[stock_result.index(i)])
    except:
        stock_re.append("-")

results['Result Date'] = stock_re

pd.set_option('display.max_colwidth', None)
results.index+=1
st.table(results)
