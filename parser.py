import requests, time
from bs4 import BeautifulSoup

import pandas as pd

from tqdm import tqdm

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By



def load_sku(file_name):
    df = pd.read_excel(file_name)
    return df[27000:]

class ParserInfoAll:

    def __init__(self) -> None:
        print('init parser')
        self.options = Options()
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)
                
        self.driver.get('https://infoprice.by/')
        time.sleep(3)
        albums =  self.driver.find_element(By.CLASS_NAME,'form-search')
        albums.click()
        time.sleep(2)
        #<button type="button" class="btn btn-primary">Да</button>
        self.driver.find_element(By.CLASS_NAME,'btn-primary').click()
        print('click')

    def get_price(self, html):

        self.driver.get(html)
        time.sleep(4)
        
        try:
            name = self.driver.find_element(By.CSS_SELECTOR, 'div.max-height')
            #print(name.text)
            return name.text
        except:
            return 'Нет данных'
        
                            
            

def reports():
    print('Начинаем парсинг')
    goods=0
    sku = load_sku('excel/bc_new1.xlsx').fillna('')
    result_dict = {'name':[],'barcode':[]}
    infoprice = ParserInfoAll()
    barcodes = sku['barcode']
    for barcode in tqdm(barcodes):
        link = 'https://infoprice.by/?search=' + str(barcode).strip() 
        name = infoprice.get_price(link)
        if name != 'Нет данных':
            goods = goods + 1
            result_dict['name'].append(name)
            result_dict['barcode'].append(str(int(barcode)))
            print(goods)
            
    result_df = pd.DataFrame.from_dict(result_dict)
    result_df = result_df.fillna(0.0)
    result_df.to_excel('excel/2/ready_bc_30.xlsx')
    
if __name__ == '__main__':
    reports()
                


