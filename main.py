import pandas as pd
import requests, json

from api import headers, params

def get_main_group():
    data_group = '{"CRC":"","Packet":{"FromId":"10003001","ServerKey":"omt5W465fjwlrtxcEco97kew2dkdrorqqq","Data":{}}}'
    response = requests.post('https://api.infoprice.by/InfoPrice.GoodsGroup', params=params, headers=headers, data=data_group)
    main_group = response.json()
    main_group_dict = {}
    for i in main_group['Table']:
        main_group_dict[i['GoodsGroupName']] = [i['GoodsGroupId'], i['Child']]
    return main_group_dict

def get_contractor():
    data_contractor = '{"CRC":"","Packet":{"FromId":"10003001","ServerKey":"omt5W465fjwlrtxcEco97kew2dkdrorqqq","Data":{"OrderBy":0,"CatalogType":1}}}'
    response = requests.post('https://api.infoprice.by/InfoPrice.Contractors', params=params, headers=headers, data=data_contractor)
    main_contractor = response.json()
    main_contractor_dict = {}
    for i in main_contractor['Table']:
        main_contractor_dict[i['ContractorName']] = i['ContractorId']
    return main_contractor_dict

def get_subcategory(groups):
    for group in groups:
        return [i for i in groups[group][1]]
            
def get_price_group(group):
    data_price =  '{"CRC":"","Packet":{"FromId":"10003001","ServerKey":"omt5W465fjwlrtxcEco97kew2dkdrorqqq","Data":{"ContractorId":"","GoodsGroupId":"3285","Page":"","Search":"","OrderBy":0,"OrderByContractor":0,"CompareСontractorId":72631,"CatalogType":1,"IsAgeLimit":0,"IsPromotionalPrice":0}}}'.encode()
    response = requests.post('https://api.infoprice.by/InfoPrice.Goods', params=params, headers=headers, data=data_price)
    price_group = response.json()
    #price_group_dict = {}
    return price_group

def get_data_group(prices_group):
    df_main = pd.DataFrame(columns=['category', 'subcategory', 'name', 'sosedi', 'korona', 'gippo', 'evroopt', 'santa', 'green'])
    
    for goods in prices_group['Table']:
        
        for data_good in goods['GoodsOffer']:
            goods_group_name = data_good['GoodsGroupName']
            goods_name = data_good['GoodsName']
            print(goods_name)
            sosedi, korona, gippo, evroopt, santa, green = 0, 0, 0, 0, 0, 0
            for price_contractor in data_good['Offers']:
                
                if price_contractor['ContractorId'] == 72494:
                    sosedi = price_contractor['Price']
                if price_contractor['ContractorId'] == 72512:
                    korona = price_contractor['Price'] 
                if price_contractor['ContractorId'] == 72511:
                    gippo =  price_contractor['Price'] 
                if price_contractor['ContractorId'] == 72517:
                    evroopt =  price_contractor['Price'] 
                if price_contractor['ContractorId'] == 72468:
                    santa =  price_contractor['Price']
                if price_contractor['ContractorId'] == 72526:
                    green =  price_contractor['Price'] 
            row = ['new', goods_group_name, goods_name, sosedi, korona, gippo, evroopt, santa, green]
                
            df_main.loc[len(df_main)] = row
                
    df_main.to_excel('1.xlsx')           
                
                

def main():
    price_group = get_price_group('3281')
    
    get_data_group(price_group)
    
    #get_data_group(data_good)



if __name__ == '__main__':
    main()