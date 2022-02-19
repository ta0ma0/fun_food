import logging
import requests
import difflib
from urllib import response
from wsgiref import headers
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup


logging.basicConfig(level=logging.DEBUG, filename='funfood.log',
                    format='%(asctime)s %(name)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

pages_to_parce = 15  # Max pages for parsing.


def get_items_(url, filename, seq):
    s = requests.Session()
    retries = Retry(total=5, backoff_factor=1,
                    status_forcelist=[502, 503, 504])
    s.mount('https://', HTTPAdapter(max_retries=retries))
    page = s.get(url)
    logger.info(f'Page {url} answered {page.status_code}')

    with open(f'data/{filename}_{seq}', 'w') as f:
        f.write(page.text)
        logger.info(f'File data/{filename}_{seq} writing on disk')

    try:
        seq = int(seq)-1
        seq = str(seq)
        with open(f'data/{filename}_{seq}') as read_f:
            previous_page = read_f.read()
    except FileNotFoundError as err:
        logger.error(f'File  data/{filename}_{seq}  not found erase or not must exist {err}')
        previous_page = ''
        pass

    try:
        current_page = BeautifulSoup(page.text, 'html.parser')
        previous_page = BeautifulSoup(previous_page, 'html.parser')
        diff_page_2 = current_page.find('div', class_='dixyCatalogItem__title')
        diff_page_1 = previous_page.find(
            'div', class_='dixyCatalogItem__title')
    except Exception as err:
        logger.error(err)
        pass
        """
        Skip parsing if pages the same, catalog is over
        """
    return [diff_page_1, diff_page_2]


def download_pages(base_url, number_of_pages, filename):
    for sequence in range(number_of_pages):
        html_diff = get_items_(f'{base_url}?sPAGEN_1={sequence}', f'{filename}', sequence)

        try:
            if html_diff[0] == html_diff[1] and sequence >= 2:
                logger.info('Catalog is over, stop downloading go parse')
                break
        except Exception as err:
            logger.info('Pass, empty page', err)
            pass
    return sequence

# for el in category_list_urls: #For test
#     f_name = get_file_name(el)
#     print(f_name[-2])
