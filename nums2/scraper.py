import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup as bs
import os

##

src = 'https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_daily_reports'
path = '/run/Parts/Exch/Sync/swap/pyt/corona/nums2/'

source = requests.get(src).text
soup = bs(source, 'lxml')

##

csv_links = [[link['href'].split('/')[-1], "https://raw.githubusercontent.com"+link['href'][:25]+link['href'][30:]] for link in soup.find_all('a', class_='js-navigation-open') if link['href'][-4:] == '.csv']
csv_links

##

csv_saved = [x for x in os.listdir('./data')]

csv_to_download = [x for x in csv_links if x[0] not in csv_saved]

##

for x in csv_to_download:
    print(x)
    name = x[0]
    df = pd.read_csv(x[1])
    df.to_csv('data/'+name)
