"""Util functions for python"""
import csv
import logging
import re
from playsound import playsound
from colorlog import ColoredFormatter

from web_info import WebInfo, SUPPORTED_WEB_LIST

LOG_FORMAT_SIMPLE = '%(asctime)s %(levelname)s : %(message)s'
LOG_FORMAT_FULL = "%(log_color)s%(levelname)s%(reset)s | %(log_color)s%(message)s%(reset)s"


WEB_NAME_TO_TYPE = {
    'www.bestbuy.ca': 'BestBuy',
    'www.newegg.ca': 'NewEgg',
}


def init_logger(logger_file_name: str):
    logging.basicConfig(filename=logger_file_name,
                        filemode='w',
                        level=logging.INFO,
                        format=LOG_FORMAT_SIMPLE)
    formatter = ColoredFormatter(LOG_FORMAT_FULL)
    stream = logging.StreamHandler()
    stream.setLevel(logging.INFO)
    stream.setFormatter(formatter)
    logging.getLogger('').addHandler(stream)


def analyze_url(url):
    token = url.split('/')
    web_name_index = 0 if token[0] == 'https' else 2
    web_type = WEB_NAME_TO_TYPE[token[web_name_index]]
    if not web_type:
        return None
    if web_type == 'BestBuy' and token[web_name_index+2] == 'product'and token[web_name_index+3] is not None:
        name = token[web_name_index+3]
    elif web_type == 'NewEgg' and token[web_name_index+1] == 'Product':
        web_type = 'NewEgg_Combo'
        name = token[web_name_index + 2].split('=')[1]
    elif web_type == 'NewEgg' and token[web_name_index+1] is not None:
        name = token[web_name_index + 1]
    return [web_type, name, url]


def process_soup(soup, web_info):
    availabilityMessage = soup.find(web_info.trace_type, class_=re.compile(web_info.trace_tag))
    if not availabilityMessage:
        logging.error(f'Cannot trace availabilityMessage from tag {web_info.trace_tag}.')
        return False
    if not availabilityMessage.text:
        logging.error('Cannot find text in availabilityMessage.')
        return False
    # print(availabilityMessage.text)
    return availabilityMessage.text not in web_info.available_message


def get_web_list(web_list_str):
    web_list = {}
    with open(web_list_str) as web_list_csv:
        csv_reader = csv.reader(web_list_csv, delimiter=',')
        for row in csv_reader:
            if len(row) == 0 or row[0] == '':
                continue
            analyzed_url = analyze_url(row[0])
            web_list[analyzed_url[1]] = WebInfo.GetWebInfo(analyzed_url[2], analyzed_url[0])
    return web_list


def notify():
    playsound('sweep.wav')
    playsound('sweep.wav')
    playsound('sweep.wav')
