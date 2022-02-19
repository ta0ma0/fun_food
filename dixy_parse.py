from cmath import pi
from  bs4 import BeautifulSoup
import datetime
# from dixy_to_db import write_db
from dixy_get import download_pages
from os.path import exists

number_of_pages = 15
dixy_products_data_all = []
seq = 0
url_base = f'https://dixy.ru/catalog/molochnaya-gastronomiya/?sections=molochnaya-gastronomiya%2F&PAGEN_1='
file_name_base = 'dixy_molochnaya-gastronomiya.txt'
counter = 0

category_list_urls = ['https://dixy.ru/catalog/molochnaya-gastronomiya/',\
                      'https://dixy.ru/catalog/ovoshchi-i-frukty/',\
                      'https://dixy.ru/catalog/myaso-yaytso/',\
                      'https://dixy.ru/catalog/krupy-zavtraki-spetsii/',\
                      'https://dixy.ru/catalog/konditerskie-izdeliya/'
                    ]

def get_file_name(category_url):
    filename_base = category_url.split('/')
    return filename_base


for category_url in category_list_urls:
    index = counter
    file_name_base_list = get_file_name(category_url)
    file_name_base = file_name_base_list[-2]
    base_url = category_list_urls[index]
    counter += 1

    print(base_url)
    print(file_name_base)
    
    seq = download_pages(base_url, number_of_pages, file_name_base)
    
    if exists(f'data/{file_name_base}_{seq}'):
        with open(f'data/{file_name_base}_{seq}') as file:
            print('читаю файл')
            source =  file.read()
            soup = BeautifulSoup(source, 'html.parser')
            raw_data = soup.find('div', class_='items products')
            cards_item = raw_data.find_all('div', class_='dixyCatalogItem')
            for el in cards_item:
                dixy_products_data = []
                price_rur_tag = el.find('div', class_='dixyCatalogItemPrice__new').p
                price_kop_tag = el.find('div', class_='dixyCatalogItemPrice__kopeck')
                price_rur = price_rur_tag.text.replace(" ", "")
                price_kop = price_kop_tag.text.replace(" ", "").lstrip()
                price_end = float(price_rur + '.' + price_kop)

                title_qty = el.find('div', class_='dixyModal__title').text
                title_qty_list = title_qty.split(',')
                if len(title_qty_list) == 1:
                    title_qty_list = title_qty.split(' ')
                    title = title_qty_list[0] + ' ' + title_qty_list[1]
                    qty = title_qty_list[-1].split('\xa0')
                    try:
                        mesure = qty[1].rstrip()
                    except Exception as er:
                        print('no mesure set null')
                        mesure = 'уп'
                    now = datetime.datetime(2022, 1, 1, 00, 00, 00)
                    str_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    dixy_products_data.append(title)
                    dixy_products_data.append(price_end)
                    dixy_products_data.append(qty[0])
                    dixy_products_data.append(mesure)
                    dixy_products_data.append(str_now)
                    dixy_products_data_all.append(dixy_products_data)
                else:
                    title = title_qty_list[0]
                    try:
                        qty = title_qty_list[1].split('\xa0')
                    except IndexError as err:
                        qty = 'None'
                    try:
                        mesure = qty[1].rstrip()
                    except Exception as er:
                        print('no mesure set null')
                        mesure = 'уп'
                    now = datetime.datetime(2022, 1, 1, 00, 00, 00)
                    str_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    dixy_products_data.append(title)
                    dixy_products_data.append(price_end)
                    dixy_products_data.append(qty[0])
                    dixy_products_data.append(mesure)
                    dixy_products_data.append(str_now)
                    dixy_products_data_all.append(dixy_products_data)

            else:
                pass
                        # write_db(dixy_products_data_all)

for el in dixy_products_data_all:
    print(el)
