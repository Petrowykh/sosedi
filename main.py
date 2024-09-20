import pandas as pd
import requests, json

from api import headers, params

from tqdm import tqdm

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
    
    df_main = pd.DataFrame(columns=['good_id', 'category', 'subcategory', 'name', 'link', 'sosedi', 'korona', 'gippo', 'evroopt', 'santa', 'green'])
    df_main_promo = pd.DataFrame(columns=['good_id', 'sosedi_promo', 'korona_promo', 'gippo_promo', 'evroopt_promo', 'santa_promo', 'green_promo'])
    #main_group = get_main_group()


    main_group = {'Промтовары, сезонные товары и товары для домашних животных': [3476,
  [{'GoodsGroupId': 3498,
    'GoodsGroupName': 'Бытовая химия',
    'IsAgeLimit': 0,
    'Child': [{'GoodsGroupId': 3500,
      'GoodsGroupName': 'Инсектициды и репелленты',
      'IsAgeLimit': 0},
     {'GoodsGroupId': 3499,
      'GoodsGroupName': 'Кондиционеры, ополаскиватели, отбеливатели и прочее',
      'IsAgeLimit': 0},
     {'GoodsGroupId': 3501,
      'GoodsGroupName': 'Мыло хозяйственное',
      'IsAgeLimit': 0},
     {'GoodsGroupId': 3527,
      'GoodsGroupName': 'Освежители воздуха',
      'IsAgeLimit': 0},
     {'GoodsGroupId': 3502,
      'GoodsGroupName': 'Средства для мытья посуды',
      'IsAgeLimit': 0},
     {'GoodsGroupId': 3503,
      'GoodsGroupName': 'Средства для ухода и уборки комнат',
      'IsAgeLimit': 0},
     {'GoodsGroupId': 3525,
      'GoodsGroupName': 'Средства для ухода и уборки кухни',
      'IsAgeLimit': 0},
     {'GoodsGroupId': 3526,
      'GoodsGroupName': 'Средства для ухода, уборки ванной и туалета',
      'IsAgeLimit': 0},
     {'GoodsGroupId': 3504,
      'GoodsGroupName': 'Стиральные порошки (гели, капсулы и прочее)',
      'IsAgeLimit': 0}]},
   {'GoodsGroupId': 3505,
    'GoodsGroupName': 'Галантерея, обувь, одежда',
    'IsAgeLimit': 0,
    'Child': [{'GoodsGroupId': 3549,
      'GoodsGroupName': 'Домашний текстиль',
      'IsAgeLimit': 0},
     {'GoodsGroupId': 3506,
      'GoodsGroupName': 'Обувная косметика и сопутствующие товары',
      'IsAgeLimit': 0},
     {'GoodsGroupId': 3530,
      'GoodsGroupName': 'Обувь, одежда',
      'IsAgeLimit': 0},
     {'GoodsGroupId': 3528,
      'GoodsGroupName': 'Средства по уходу за одеждой и сопутствующие товары',
      'IsAgeLimit': 0},
     {'GoodsGroupId': 3548,
      'GoodsGroupName': 'Сумки, зонты, кошельки, портмоне и прочее',
      'IsAgeLimit': 0},
     {'GoodsGroupId': 3614,
      'GoodsGroupName': 'Часы, аксессуары',
      'IsAgeLimit': 0},
     {'GoodsGroupId': 3529,
      'GoodsGroupName': 'Чулочно-носочные изделия',
      'IsAgeLimit': 0}]},
   {'GoodsGroupId': 3561,
    'GoodsGroupName': 'Досуг и развлечения ',
    'IsAgeLimit': 0,
    'Child': [{'GoodsGroupId': 3562,
      'GoodsGroupName': 'Досуг и развлечения, настольные игры',
      'IsAgeLimit': 0},
     {'GoodsGroupId': 3619,
      'GoodsGroupName': 'Охота и рыбалка',
      'IsAgeLimit': 0},
     {'GoodsGroupId': 3563,
      'GoodsGroupName': 'Товары для рукоделия',
      'IsAgeLimit': 0}]},
   {'GoodsGroupId': 3532,
    'GoodsGroupName': 'Канцелярские товары',
    'IsAgeLimit': 0,
    'Child': [{'GoodsGroupId': 3533,
      'GoodsGroupName': 'Канцелярские товары, школьные принадлежности',
      'IsAgeLimit': 0},
     {'GoodsGroupId': 3550,
      'GoodsGroupName': 'Учебники, книги, журналы и прочее',
      'IsAgeLimit': 0}]},
   {'GoodsGroupId': 3507,
    'GoodsGroupName': 'Косметика и парфюмерия',
    'IsAgeLimit': 0,
    'Child': [{'GoodsGroupId': 3531,
      'GoodsGroupName': 'Декоративная косметика, аксессуары',
      'IsAgeLimit': 0},
     {'GoodsGroupId': 3508,
      'GoodsGroupName': 'Мыло и средства для интимной гигиены',
      'IsAgeLimit': 0},
     {'GoodsGroupId': 3509,
      'GoodsGroupName': 'Наборы косметические',
      'IsAgeLimit': 0},
     {'GoodsGroupId': 3510,
      'GoodsGroupName': 'Парфюмерия дезодоранты',
      'IsAgeLimit': 0},
     {'GoodsGroupId': 3511,
      'GoodsGroupName': 'Средства для душа и принятия ванны, аксессуары',
      'IsAgeLimit': 0},
     {'GoodsGroupId': 3512,
      'GoodsGroupName': 'Средства для ухода за волосами и аксессуары',
      'IsAgeLimit': 0},
     {'GoodsGroupId': 3513,
      'GoodsGroupName': 'Средства для/после бритья и депиляции',
      'IsAgeLimit': 0},
     {'GoodsGroupId': 3514,
      'GoodsGroupName': 'Средства по уходу за лицом, телом и аксессуары',
      'IsAgeLimit': 0},
     {'GoodsGroupId': 3515,
      'GoodsGroupName': 'Средства по уходу за полостью рта',
      'IsAgeLimit': 0}]},
   {'GoodsGroupId': 3551,
    'GoodsGroupName': 'Спортивные товары',
    'IsAgeLimit': 0,
    'Child': [{'GoodsGroupId': 3552,
      'GoodsGroupName': 'Спортивные товары, туризм',
      'IsAgeLimit': 0}]},
   {'GoodsGroupId': 3479,
    'GoodsGroupName': 'Средства индивидуальной защиты и медицинские средства',
    'IsAgeLimit': 0,
    'Child': [{'GoodsGroupId': 3480,
      'GoodsGroupName': 'Контрацептивы, гели-лубриканты',
      'IsAgeLimit': 0},
     {'GoodsGroupId': 3481,
      'GoodsGroupName': 'Средства медицинского назначения',
      'IsAgeLimit': 0}]},
   {'GoodsGroupId': 3482,
    'GoodsGroupName': 'Товары для гигиены',
    'IsAgeLimit': 0,
    'Child': [{'GoodsGroupId': 3483,
      'GoodsGroupName': 'Бумажная продукция (салфетки, полотенца, прочее)',
      'IsAgeLimit': 0},
     {'GoodsGroupId': 3484,
      'GoodsGroupName': 'Ватные диски и палочки',
      'IsAgeLimit': 0},
     {'GoodsGroupId': 3523,
      'GoodsGroupName': 'Влажные салфетки',
      'IsAgeLimit': 0},
     {'GoodsGroupId': 3485,
      'GoodsGroupName': 'Подгузники и простыни для взрослых',
      'IsAgeLimit': 0},
     {'GoodsGroupId': 3486,
      'GoodsGroupName': 'Товары женской гигиены',
      'IsAgeLimit': 0}]},
   {'GoodsGroupId': 3487,
    'GoodsGroupName': 'Товары для домашних животных',
    'IsAgeLimit': 0,
    'Child': [{'GoodsGroupId': 3491,
      'GoodsGroupName': 'Аксессуары, игрушки, наполнители',
      'IsAgeLimit': 0},
     {'GoodsGroupId': 3488,
      'GoodsGroupName': 'Корма для кошек',
      'IsAgeLimit': 0},
     {'GoodsGroupId': 3489,
      'GoodsGroupName': 'Корма для собак',
      'IsAgeLimit': 0},
     {'GoodsGroupId': 3490,
      'GoodsGroupName': 'Прочие корма',
      'IsAgeLimit': 0}]},
   {'GoodsGroupId': 3557,
    'GoodsGroupName': 'Товары для праздника ',
    'IsAgeLimit': 0,
    'Child': [{'GoodsGroupId': 3558,
      'GoodsGroupName': 'Товары для праздника',
      'IsAgeLimit': 0}]},
   {'GoodsGroupId': 3492,
    'GoodsGroupName': 'Хозяйственные товары',
    'IsAgeLimit': 0,
    'Child': [{'GoodsGroupId': 3553,
      'GoodsGroupName': 'Садовый инвентарь ',
      'IsAgeLimit': 0},
     {'GoodsGroupId': 3604,
      'GoodsGroupName': 'Сантехника и аксессуары ',
      'IsAgeLimit': 0},
     {'GoodsGroupId': 3497,
      'GoodsGroupName': 'Товары для дачи, отдых на природе',
      'IsAgeLimit': 0},
     {'GoodsGroupId': 3555,
      'GoodsGroupName': 'Товары для строительства и ремонта ',
      'IsAgeLimit': 0},
     {'GoodsGroupId': 3493,
      'GoodsGroupName': 'Хозяйственные товары для ванной и туалета, аксессуары для сантехники',
      'IsAgeLimit': 0},
     {'GoodsGroupId': 3496,
      'GoodsGroupName': 'Хозяйственные товары для уборки',
      'IsAgeLimit': 0},
     {'GoodsGroupId': 3494,
      'GoodsGroupName': 'Хозяйственные товары и аксессуары для дома',
      'IsAgeLimit': 0},
     {'GoodsGroupId': 3495,
      'GoodsGroupName': 'Хозяйственные товары и аксессуары для кухни',
      'IsAgeLimit': 0}]}]]}
    for main_name in main_group:
        print(main_name)
        for group_id in tqdm(main_group[main_name][1]):  
            # block with actual price 
            ################################################################
            price = get_price_group(group_id['GoodsGroupId'], "")
            print(group_id['GoodsGroupId'])
            for page in tqdm(range(0, price['Table'][0]['GeneralData'][0]['AmountPages'])):
                
                prices_group = get_price_group(group_id['GoodsGroupId'], str(page))
                for goods in prices_group['Table']:
                    #print(goods, "\n")
                    if (goods['GeneralData'][0]['AmountGoods'] != 0) and ('GoodsOffer' in goods) :
                        # delete slice
                        for data_good in goods['GoodsOffer']:
                            
                            goods_group_name = data_good['GoodsGroupName']
                            goods_name = data_good['GoodsName']
                            goods_id = data_good['GoodsId']
                            
                            sosedi, korona, gippo, evroopt, santa, green = 0.00, 0.00, 0.00, 0.00, 0.00, 0.00
                            for price_contractor in data_good['Offers']:
                                #TODO тут проверяем условие
                                if price_contractor['ContractorId'] == 72494:
                                    sosedi = float(price_contractor['Price'])
                                if price_contractor['ContractorId'] == 72512:
                                    korona = float(price_contractor['Price'])
                                if price_contractor['ContractorId'] == 72511:
                                    gippo =  float(price_contractor['Price'])
                                if price_contractor['ContractorId'] == 72517:
                                    evroopt = float(price_contractor['Price'])
                                if price_contractor['ContractorId'] == 72468:
                                    santa =  float(price_contractor['Price'])
                                if price_contractor['ContractorId'] == 72526:
                                    green =  float(price_contractor['Price'] )
                            if any([sosedi, korona, gippo, evroopt, santa, green]):
                                link = 'https://infoprice.by/?search=' + "+".join(goods_name.split(" "))
                                df_main.loc[len(df_main)] = [goods_id, main_name, goods_group_name, goods_name, link, sosedi, korona, gippo, evroopt, santa, green]
                            link = 'https://infoprice.by/?search=' + "+".join(goods_name.split(" "))
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
                            
                            sosedi_promo, korona_promo, gippo_promo, evroopt_promo, santa_promo, green_promo = 0.00, 0.00, 0.00, 0.00, 0.00, 0.00
                            for price_contractor in data_good['Offers']:
                                #TODO тут проверяем условие
                                if price_contractor['ContractorId'] == 72494 and price_contractor['IsPromotionalPrice']:
                                    sosedi_promo = float(price_contractor['Price'])
                                if price_contractor['ContractorId'] == 72512 and price_contractor['IsPromotionalPrice']:
                                    korona_promo = float(price_contractor['Price']) 
                                if price_contractor['ContractorId'] == 72511 and price_contractor['IsPromotionalPrice']:
                                    gippo_promo =  float(price_contractor['Price']) 
                                if price_contractor['ContractorId'] == 72517 and price_contractor['IsPromotionalPrice']:
                                    evroopt_promo = float(price_contractor['Price']) 
                                if price_contractor['ContractorId'] == 72468 and price_contractor['IsPromotionalPrice']:
                                    santa_promo = float(price_contractor['Price'])
                                if price_contractor['ContractorId'] == 72526 and price_contractor['IsPromotionalPrice']:
                                    green_promo = float(price_contractor['Price']) 
                            if any([sosedi_promo, korona_promo, gippo_promo, evroopt_promo, santa_promo, green_promo]):
                                df_main_promo.loc[len(df_main_promo)] = [goods_id, sosedi_promo, korona_promo, gippo_promo, evroopt_promo, santa_promo, green_promo]   

    result = pd.merge(df_main, df_main_promo, how='left', on='good_id').fillna(0)
    result = result[['category', 'subcategory', 'name', 'link', 'sosedi', 'sosedi_promo', 'korona', 'korona_promo', 'gippo', 'gippo_promo', 'evroopt', 'evroopt_promo', 'santa', 'santa_promo', 'green', 'green_promo']]


    result.to_excel('1.xlsx')    
        
                
                

def main():
    #price_group = get_price_group('3281')
    
    get_data_group()

    #get_subcategory(get_main_group())
    
    
   



if __name__ == '__main__':
    main()


if __name__ == '__main__':
    main()