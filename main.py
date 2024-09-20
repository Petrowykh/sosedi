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
    third_part = '","Search":"","OrderBy":0,"OrderByContractor":0,"CompareСontractorId":72631,"CatalogType":1,"IsAgeLimit":0,"IsPromotionalPrice":0}}}'
    #TODO тут меняем на 0
    return (first_part + str(group_id) + second_part + page + third_part).encode()          

def create_data_group_promo(group_id, page=""):
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

def get_price_group_promo(group_id, page):
    data_price =  create_data_group_promo(group_id, page=page)
    response = requests.post('https://api.infoprice.by/InfoPrice.Goods', params=params, headers=headers, data=data_price)
    price_group = response.json()
    
    return price_group

def get_data_group():
    
    df_main = pd.DataFrame(columns=['good_id', 'category', 'subcategory', 'name', 'sosedi', 'korona', 'gippo', 'evroopt', 'santa', 'green'])
    df_main_promo = pd.DataFrame(columns=['good_id', 'sosedi_promo', 'korona_promo', 'gippo_promo', 'evroopt_promo', 'santa_promo', 'green_promo'])
    #main_group = get_main_group()
    main_group = {'Овощи и фрукты': [3280, [{'GoodsGroupId': 3281, 'GoodsGroupName': 'Овощи и фрукты', 'IsAgeLimit': 0, 'Child': [{'GoodsGroupId': 3282, 'GoodsGroupName': 'Овощи, грибы', 'IsAgeLimit': 0}, {'GoodsGroupId': 3283, 'GoodsGroupName': 'Фрукты, ягоды', 'IsAgeLimit': 0}]}]], 'Алкоголь': [3284, [{'GoodsGroupId': 3285, 'GoodsGroupName': 'Вино, игристые', 'IsAgeLimit': 1, 'Child': [{'GoodsGroupId': 3286, 'GoodsGroupName': 'Вино импортное', 'IsAgeLimit': 1}, {'GoodsGroupId': 3287, 'GoodsGroupName': 'Вино плодово-ягодное', 'IsAgeLimit': 1}, {'GoodsGroupId': 3288, 'GoodsGroupName': 'Вино РБ', 'IsAgeLimit': 1}, {'GoodsGroupId': 3289, 'GoodsGroupName': 'Игристые вина, шампанское', 'IsAgeLimit': 1}]}, {'GoodsGroupId': 3290, 'GoodsGroupName': 'Крепкий алкоголь', 'IsAgeLimit': 1, 'Child': [{'GoodsGroupId': 3291, 'GoodsGroupName': 'Бренди, коньяк', 'IsAgeLimit': 1}, {'GoodsGroupId': 3293, 'GoodsGroupName': 'Вермут, ликеры, бальзамы, настойки', 'IsAgeLimit': 1}, {'GoodsGroupId': 3292, 'GoodsGroupName': 'Виски, ром, текила, джин, прочее', 'IsAgeLimit': 1}, {'GoodsGroupId': 3518, 'GoodsGroupName': 'Водка', 'IsAgeLimit': 1}]}, {'GoodsGroupId': 3294, 'GoodsGroupName': 'Пиво', 'IsAgeLimit': 1, 'Child': [{'GoodsGroupId': 3295, 'GoodsGroupName': 'Пиво в жестяной банке', 'IsAgeLimit': 1}, {'GoodsGroupId': 3297, 'GoodsGroupName': 'Пиво в ПЭТ', 'IsAgeLimit': 1}, {'GoodsGroupId': 3296, 'GoodsGroupName': 'Пиво в стекле', 'IsAgeLimit': 1}]}, {'GoodsGroupId': 3298, 'GoodsGroupName': 'Слабоалкогольные напитки', 'IsAgeLimit': 1, 'Child': [{'GoodsGroupId': 3299, 'GoodsGroupName': 'Слабоалкогольные напитки', 'IsAgeLimit': 1}]}]]}
    for main_name in main_group:
        
        for group_id in main_group[main_name][1]:  
            # block with actual price 
            ################################################################
            price = get_price_group(group_id['GoodsGroupId'], "")
            for page in range(0, price['Table'][0]['GeneralData'][0]['AmountPages']):
                print(group_id['GoodsGroupId'], page)
                prices_group = get_price_group(group_id['GoodsGroupId'], str(page))
                for goods in prices_group['Table']:
                    #print(goods, "\n")
                    if (goods['GeneralData'][0]['AmountGoods'] != 0) and ('GoodsOffer' in goods) :
                        # delete slice
                        for data_good in goods['GoodsOffer']:
                            
                            goods_group_name = data_good['GoodsGroupName']
                            goods_name = data_good['GoodsName']
                            goods_id = data_good['GoodsId']
                            
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
                                df_main.loc[len(df_main)] = [goods_id, main_name, goods_group_name, goods_name, sosedi, korona, gippo, evroopt, santa, green]
            
            # block with promo price
           
            price_promo = get_price_group_promo(group_id['GoodsGroupId'], "")
            for page in range(0, price_promo['Table'][0]['GeneralData'][0]['AmountPages']):
                prices_group_promo = get_price_group_promo(group_id['GoodsGroupId'], str(page))
                for goods_promo in prices_group_promo['Table']:
                    #print(goods, "\n")
                    if (goods_promo['GeneralData'][0]['AmountGoods'] != 0) and ('GoodsOffer' in goods_promo) :
                        # delete slice
                        for data_good in goods_promo['GoodsOffer']:
                            goods_name = data_good['GoodsName']
                            goods_id = data_good['GoodsId']
                            
                            sosedi_promo, korona_promo, gippo_promo, evroopt_promo, santa_promo, green_promo = 0, 0, 0, 0, 0, 0
                            for price_contractor in data_good['Offers']:
                                #TODO тут проверяем условие
                                if price_contractor['ContractorId'] == 72494 and price_contractor['IsPromotionalPrice']:
                                    sosedi_promo = price_contractor['Price']
                                if price_contractor['ContractorId'] == 72512 and price_contractor['IsPromotionalPrice']:
                                    korona_promo = price_contractor['Price'] 
                                if price_contractor['ContractorId'] == 72511 and price_contractor['IsPromotionalPrice']:
                                    gippo_promo =  price_contractor['Price'] 
                                if price_contractor['ContractorId'] == 72517 and price_contractor['IsPromotionalPrice']:
                                    evroopt_promo =  price_contractor['Price'] 
                                if price_contractor['ContractorId'] == 72468 and price_contractor['IsPromotionalPrice']:
                                    santa_promo =  price_contractor['Price']
                                if price_contractor['ContractorId'] == 72526 and price_contractor['IsPromotionalPrice']:
                                    green_promo =  price_contractor['Price'] 
                            if any([sosedi_promo, korona_promo, gippo_promo, evroopt_promo, santa_promo, green_promo]):
                                df_main_promo.loc[len(df_main_promo)] = [goods_id, sosedi_promo, korona_promo, gippo_promo, evroopt_promo, santa_promo, green_promo]   

    result = pd.merge(df_main, df_main_promo, how='left', on='good_id').fillna(0)
    result.to_excel('1.xlsx')    
        
                
                

def main():
    #price_group = get_price_group('3281')
    
    get_data_group()

    #get_subcategory(get_main_group())
    
    
   



if __name__ == '__main__':
    main()