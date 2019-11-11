import numpy as np # linear algebra
import pandas as pd # pandas for dataframe based data processing and CSV file I/O

import requests # for http requests
from bs4 import BeautifulSoup # for html parsing and scraping
from fastnumbers import isfloat
from fastnumbers import fast_float
from multiprocessing.dummy import Pool as ThreadPool
import bs4

import matplotlib.pyplot as plt
import seaborn as sns
import json
# from tidylib import tidy_document # for tidying incorrect html

sns.set_style('whitegrid')
# %matplotlib inline
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

def ffloat(string):
    if string is None:
        return np.nan
    if type(string)==float or type(string)==np.float64:
        return string
    if type(string)==int or type(string)==np.int64:
        return string
    return fast_float(string.split(" ")[0].replace(',','').replace('%',''),
                      default=np.nan)

def ffloat_list(string_list):
    return list(map(ffloat,string_list))

def remove_multiple_spaces(string):
    if type(string)==str:
        return ' '.join(string.split())
    return string
response = requests.get("http://www.example.com/", timeout=240)
response.status_code
response.content

url = "https://jsonplaceholder.typicode.com/posts/1"
response = requests.get(url, timeout=240)
response.status_code
response.json()

content = response.json()
content.keys()

def request_with_check(url):
    page_response = requests.get(url, timeout=240)
    status = page_response.status_code
    if status>299:
        raise AssertionError("page content not found, status: %s"%status)
    return page_response

# request_with_check("https://www.google.co.in/mycustom404page")


request_with_check("https://www.google.co.in/")


from IPython.core.display import HTML
HTML("<b>Rendered HTML</b>")

page_response = requests.get("https://www.moneycontrol.com/india/stockpricequote/auto-2-3-wheelers/heromotocorp/HHM", timeout=240)
page_content = BeautifulSoup(page_response.content, "html.parser")
HTML(str(page_content.find("h1")))

HTML(str(page_content.find("div",attrs={'id':"content_full"})))

page_response = requests.get("https://www.moneycontrol.com/india/stockpricequote/auto-2-3-wheelers/heromotocorp/HHM", timeout=240)
page_content = BeautifulSoup(page_response.content, "html.parser")
price_div = page_content.find("div",attrs={"id":'b_changetext'})
HTML(str(price_div))

page_content.find_all("p")
page_content.find("p",attrs={"class":"my-id"})
page_content.find_all("p",attrs={"id":"my-id"})
page_content.find_all("p",attrs={"id":"my-id"})


#list(price_div.children)


def get_children(html_content):
    children = list()
    for item in html_content.children:
        if type(item) == bs4.element.Comment:
            continue
        if type(item) == bs4.element.Tag or len(str(item).replace("\n", "").strip()) > 0:
            children.append(item)

    return children

# get_children(price_div)

html = '''
<table>
    <tr>
        <td>Month</td>
        <td>Price</td>
    </tr>
    <tr>
        <td>July</td>
        <td>2</td>
    </tr>
    <tr>
        <td>August</td>
        <td>4</td>
    </tr>
    <tr>
        <td>September</td>
        <td>3</td>
    </tr>
    <tr>
        <td>October</td>
        <td>2</td>
    </tr>
</table>

'''

HTML(html)


def get_table_simple(table, is_table_tag=True):
    elems = table.find_all('tr') if is_table_tag else get_children(table)
    table_data = list()
    for row in elems:

        row_data = list()
        row_elems = get_children(row)
        for elem in row_elems:
            text = elem.text.strip().replace("\n", "")
            text = remove_multiple_spaces(text)
            if len(text) == 0:
                continue
            row_data.append(text)
        table_data.append(row_data)
    return table_data


html = BeautifulSoup(html,"html.parser")
get_table_simple(html)

html = '''
<html>
<body>
<div id="table" class="FL" style="width:210px; padding-right:10px">
    <div class="PA7 brdb">
        <div class="FL gL_10 UC">MARKET CAP (Rs Cr)</div>
        <div class="FR gD_12">63,783.84</div>
        <div class="CL"></div>
    </div>
    <div class="PA7 brdb">
        <div class="FL gL_10 UC">P/E</div>
        <div class="FR gD_12">17.27</div>
        <div class="CL"></div>
    </div>
    <div class="PA7 brdb">
        <div class="FL gL_10 UC">BOOK VALUE (Rs)</div>
        <div class="FR gD_12">589.29</div>
        <div class="CL"></div>
    </div>
    <div class="PA7 brdb">
        <div class="FL gL_10 UC">DIV (%)</div>
        <div class="FR gD_12">4750.00%</div>
        <div class="CL"></div>
    </div>
    <div class="PA7 brdb">
        <div class="FL gL_10 UC">Market Lot</div>
        <div class="FR gD_12">1</div>
        <div class="CL"></div>
    </div>
    <div class="PA7 brdb">
        <div class="FL gL_10 UC">INDUSTRY P/E</div>
        <div class="FR gD_12">19.99</div>
        <div class="CL"></div>
    </div>
</div>
</body>
</html>
'''
HTML(html)

content = BeautifulSoup(html,"html.parser")
get_table_simple(content.find("div",attrs={"id":"table"}),is_table_tag=False)


def get_scrip_info(url):
    original_url = url
    key_val_pairs = {}

    page_response = requests.get(url, timeout=240)
    page_content = BeautifulSoup(page_response.content, "html.parser")
    price = ffloat(page_content.find('div', attrs={'span': 'span_price_wrap stprh rdclr'}).text)
    name = page_content.find('h1', attrs={'class': 'company_name'}).text

    yearly_high = page_content.find('span', attrs={'id': 'n_52high'}).text.strip()
    yearly_low = page_content.find('span', attrs={'id': 'n_52low'}).text.strip()
    html_data_content = page_content.find('div', attrs={'id': 'mktdet_1'})

    petable = get_table_simple(get_children(html_data_content)[0], is_table_tag=False)
    pbtable = get_table_simple(get_children(html_data_content)[1], is_table_tag=False)
    volume = ffloat(page_content.find('span', attrs={'id': 'nse_volume'}).text)

    data_table = list()
    data_table.extend(petable)
    data_table.extend(pbtable)

    collector = {row[0]: ffloat(row[1]) if len(row) == 2 else None for row in data_table}

    key_val_pairs["pe"] = collector['P/E']
    key_val_pairs["book_value"] = collector['BOOK VALUE (Rs)']
    key_val_pairs["deliverables"] = collector['DELIVERABLES (%)']
    if 'MARKET CAP (Rs Cr)' in collector:
        key_val_pairs["market_cap"] = collector['MARKET CAP (Rs Cr)']
    elif '**MARKET CAP (Rs Cr)' in collector:
        key_val_pairs["market_cap"] = collector['**MARKET CAP (Rs Cr)']
    key_val_pairs["pb"] = collector['PRICE/BOOK']
    key_val_pairs['price'] = price
    key_val_pairs['volume'] = volume
    key_val_pairs["yearly_low"] = ffloat(yearly_low)
    key_val_pairs["yearly_high"] = ffloat(yearly_high)
    return key_val_pairs

get_scrip_info("https://www.moneycontrol.com/india/stockpricequote/auto-2-3-wheelers/heromotocorp/HHM")