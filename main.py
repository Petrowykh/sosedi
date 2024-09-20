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

def get_subcategory(main_groups):
    x = []
    for i in main_groups:
        for j in main_groups[i][1]:
            x.append(j['GoodsGroupId'])
    print(x)

    
def create_data_group(group_id, page=""):
    first_part ='{"CRC":"","Packet":{"FromId":"10003001","ServerKey":"omt5W465fjwlrtxcEco97kew2dkdrorqqq","Data":{"ContractorId":"","GoodsGroupId":"'
    second_part = '","Page":"'
    third_part = '","Search":"","OrderBy":0,"OrderByContractor":0,"CompareСontractorId":72631,"CatalogType":1,"IsAgeLimit":0,"IsPromotionalPrice":1}}}'
    #TODO тут меняем на 0
    return (first_part + str(group_id) + second_part + page + third_part).encode()          

def get_price_group(group_id, page):
    data_price =  create_data_group(group_id, page=page)
    response = requests.post('https://api.infoprice.by/InfoPrice.Goods', params=params, headers=headers, data=data_price)
    price_group = response.json()
    
    return price_group

def get_data_group():
    
    df_main = pd.DataFrame(columns=['category', 'subcategory', 'good_id', 'name', 'sosedi', 'korona', 'gippo', 'evroopt', 'santa', 'green'])
    main_group = get_main_group()
    for main_name in main_group:
       
        for group_id in main_group[main_name][1][:5]:  
            
            price = get_price_group(group_id['GoodsGroupId'], "")
                  
            prices_group = get_price_group(group_id['GoodsGroupId'], str(price['Table'][0]['GeneralData'][0]['AmountPages']))
            for goods in prices_group['Table']:
                print(goods, "\n")
                if (goods['GeneralData'][0]['AmountGoods'] != 0) and ('GoodsOffer' in goods) :
                    for data_good in goods['GoodsOffer']:
                        
                        goods_group_name = data_good['GoodsGroupName']
                        goods_name = data_good['GoodsName']
                        goods_id = data_good['GoodsId']
                        #print(goods_name)
                        sosedi, korona, gippo, evroopt, santa, green = 0, 0, 0, 0, 0, 0
                        for price_contractor in data_good['Offers']:
                            #TODO тут проверяем условие
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
                        if any([sosedi, korona, gippo, evroopt, santa, green]):
                            row = [main_name, goods_group_name, goods_id, goods_name, sosedi, korona, gippo, evroopt, santa, green]
                            
                        df_main.loc[len(df_main)] = row
                
    df_main.to_excel('1.xlsx')           
                
                

def main():
    #price_group = get_price_group('3281')
    
    get_data_group()

    #get_subcategory(get_main_group())
    
    
   



if __name__ == '__main__':
    main()