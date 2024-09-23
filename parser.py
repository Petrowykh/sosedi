import requests, time
from bs4 import BeautifulSoup

import pandas as pd

from requests.utils import requote_uri

from tqdm import tqdm

url = 'https://barcode-list.ru/barcode/RU/%D0%9F%D0%BE%D0%B8%D1%81%D0%BA.htm?barcode='

excel_df = pd.read_excel('1.xlsx', usecols=['name'])
goods = excel_df['name'].values.tolist()

df_code = pd.DataFrame(columns=['name', 'code'])

for name in tqdm(goods):
    #name = 'Вино "Старый Тбилиси Алазани" красное п/сл. 11.5 0.75л Грузия'
    #name = name.replace('%', '')
    link = requote_uri(url + "+".join(name.split(" ")).lower())
    time.sleep(2)
    
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')
    quotes = soup.find('table', class_ ='main_table').find('td', class_ = 'main_column').find('a').text
    df_code.loc[len(df_code)] = (name, quotes)

df_code.to_excel('code.xlsx')  


