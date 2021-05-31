from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

# data = requests.get('http://www.alteclansing.com/product/alx-s15p-15-active-subwoofer/')
data = requests.get('https://www.academy.com/shop/pdp/all-star-classic-series-casting-rod#repChildCatid=4138067')

# dfs = pd.read_html(data.text)
# print(dfs)

soup = BeautifulSoup(data.text,'html.parser')
# print(soup)

# print(soup)

# description = scrape_helper.find_by_id('div', 'description')
# specs = list()
# for listitems in soup.findAll('li'):
#     if(':' in listitems.get_text()):
#         specs.append(listitems.get_text())

specs = ""
if len(specs) == 0:
    for listitems in soup.findAll('li'):
        specs += listitems.get_text()

        # specs.append(listitems.get_text())
specs = specs.replace('\n',' ')

if(':' in specs):
    for listitems in soup.findAll('li'):
        if(':' in listitems.get_text()):
            specs += listitems.get_text() + '\n'

print(specs)


# print(len(listitems))