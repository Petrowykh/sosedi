import requests, time
from bs4 import BeautifulSoup

from requests.utils import requote_uri

vine = ['Вино "Старый Тбилиси Алазани" красное п/сл. 11.5% 0.75л Грузия', 
'Вино "Черный доктор" красное п/сл 16% 0.75л Молдова',
'Вино "Cava Carta Nevada" игристое белое п/сух 12% 0.75л Испания', 
'Вино "J.P. Chenet" розовое п/сл 12% 0.75л Франция',
'Вино "Старая келья" белое п/сл 9-13% 0.7л РБ', 
'Вино "Старая келья" красное п/сл 12.5-14% 0.7л РБ', 
'Вино "Gato Negro" красное сух. 14% 0.75л Чили',
'Вино "J.P. Chenet" красное сух. 12.5-14% 0.75л Франция', 
'Вино "J.P. Chenet" красное п/сл 12.5-14% 0.75л Франция', 
'Шампанское "Советское" п/сл 10.5-12% 0.75л РБ',
'Вино "Campo Viejо" красное сух. 13.5% 0.75л Испания']

url = 'https://barcode-list.ru/barcode/RU/%D0%9F%D0%BE%D0%B8%D1%81%D0%BA.htm?barcode='



for name in vine:
    #name = 'Вино "Старый Тбилиси Алазани" красное п/сл. 11.5 0.75л Грузия'
    #name = name.replace('%', '')
    link = requote_uri(url + "+".join(name.split(" ")).lower())
    time.sleep(5)
    
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')
    quotes = soup.find('table', class_ ='main_table').find('td', class_ = 'main_column').find('a').text
    print(name, '---', quotes)



