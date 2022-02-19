from urllib import response
from wsgiref import headers
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import difflib
from  bs4  import BeautifulSoup


pages_to_parce = 15 #Max pages for parsing.




def get_items_(url, filename, seq):
    s = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[ 502, 503, 504 ])
    s.mount('https://', HTTPAdapter(max_retries=retries))
    headers_ = s.head(url)
    page = s.get(url)


    with open(f'data/{filename}_{seq}', 'w') as f:
        f.write(page.text)
    
    try:
        seq = int(seq)-1
        seq = str(seq)
        with open(f'data/{filename}_{seq}') as read_f:
            previous_page = read_f.read()
    except Exception as err:
        print('Нет файла', err)
        previous_page=''
        pass
        

    try:
        current_page = BeautifulSoup(page.text, 'html.parser')
        previous_page = BeautifulSoup(previous_page, 'html.parser')
        diff_page_2 = current_page.find('div', class_='dixyCatalogItem__title')
        diff_page_1 = previous_page.find('div', class_='dixyCatalogItem__title')
        # print(diff_page_1[0], diff_page_2[0])
        print(diff_page_1, diff_page_2)
    except Exception as err:

        pass
        """
        Skip parsing if pages the same, catalog is over
        """
    return [diff_page_1, diff_page_2]



def download_pages(base_url, number_of_pages, filename):
    for sequence in range(number_of_pages):
        html_diff = get_items_(f'{base_url}?sPAGEN_1={sequence}', f'{filename}', sequence)
        

        try:
            if html_diff[0] == html_diff[1] and sequence >=2:
                print('Catalog is over, stopping')
                break
        except Exception as err:
            print(err, 'Pass empty page')
            pass
    return sequence
        #print(sequence) #For test

# for el in category_list_urls: #For test
#     f_name = get_file_name(el)
#     print(f_name[-2])