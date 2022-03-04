import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
from pathlib import Path
import os

data_dir = './data'

source = requests.get('https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_daily_reports').text
soup = bs(source, 'lxml')

csv_links = [[link['href'].split('/')[-1], "https://raw.githubusercontent.com"+link['href'][:25]+link['href'][30:]] for link in soup.find_all('a', class_='js-navigation-open') if link['href'][-4:] == '.csv']
csv_links

Path(data_dir).mkdir(parents=True, exist_ok=True)
csv_saved = os.listdir(data_dir)
csv_to_download = [x for x in csv_links if x[0] not in csv_saved]

if csv_to_download:
    print("Downloading data for day ...")
    for x in csv_to_download:
        print(f"  {x[0][:-4]}")
        name = x[0]
        df = pd.read_csv(x[1])
        df.to_csv('data/'+name)
else:
    print("Nothing to do.")
