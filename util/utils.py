"""Util functions for python"""
import csv
import json
import logging
import re
import string
from typing import List

from playsound import playsound
from colorlog import ColoredFormatter

import web_info
from util.url_requester import request_general
from video_card_type import VideoCard
from web_info import WebInfo

LOG_FORMAT_SIMPLE = '%(asctime)s %(levelname)s : %(message)s'
LOG_FORMAT_FULL = "%(log_color)s%(levelname)s%(reset)s | %(log_color)s%(message)s%(reset)s"


WEB_NAME_TO_TYPE = {
    'www.bestbuy.ca': 'BestBuy',
    'www.newegg.ca': 'NewEgg',
    'www.pc-canada.com': 'PCCanada',
}

CRYPTO_LIST = [
    'bitcoin',
]


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
    elif web_type == 'PCCanada':
        name = token[web_name_index + 2].split('?')[0]
    return [web_type, name, url]


def process_soup(soup, web_info):
    availabilityMessage = soup.find(web_info.trace_type, class_=re.compile(web_info.trace_tag))
    if not availabilityMessage:
        logging.error(f'Cannot trace availabilityMessage from url {web_info.url}.')
        return False
    if not availabilityMessage.text:
        logging.error(f'Cannot find text in availabilityMessage from url: {web_info.url}.')
        return False
    # print(availabilityMessage.text)
    return availabilityMessage.text not in web_info.available_message


def get_web_list(web_list_str: str) -> dict:
    web_list = {}
    with open(web_list_str) as web_list_csv:
        csv_reader = csv.reader(web_list_csv, delimiter=',')
        for row in csv_reader:
            if len(row) == 0 or row[0] == '' or row[0].startswith('#'):
                continue
            analyzed_url = analyze_url(row[0])
            web_list[analyzed_url[1]] = WebInfo.GetWebInfo(analyzed_url[2], analyzed_url[0])
    return web_list


def get_video_card_list(video_card_list_str: str) -> dict:
    video_card_list = {}
    with open(video_card_list_str) as video_card_list_str_csv:
        csv_reader = csv.reader(video_card_list_str_csv, delimiter=',')
        for row in csv_reader:
            if len(row) < 2 or row[0] == '' or row[0].startswith('#'):
                continue
            strength = int(row[2]) if len(row) == 3 and row[2] != '' else None
            video_card = VideoCard(
                name=str(row[0]),
                msrp=int(row[1]),
                strength=strength,
            )
            video_card_list[video_card.name] = video_card
    return video_card_list


def analyze_video_card_type(webinfo: WebInfo, video_card_list: List[VideoCard]) -> None:
    for vc in video_card_list:
        if webinfo.url.find(vc.id_tag):
            webinfo.video_card = vc
            break


def display_video_card_list(vc_list: List[VideoCard]) -> None:
    info = "Quick fact for Video Card original price:\n"
    vc_list.sort(key=lambda x: x.get_VfM(), reverse=True)
    for vc in vc_list:
        info += f"{vc.name}    \t msrp: {vc.msrp}  \t Value for Money: {vc.VfM}\n"
    info +="========================================"
    logging.info(info)



def get_latest_crypto_price():
    TICKER_API_URL = 'https://blockchain.info/ticker'
    soup = request_general(url=TICKER_API_URL,
                           headers=web_info.DEFAULT_HEADER,
                           name_tag='bitcoin',
                           is_gzipped=True)
    return json.loads(str(soup.currentTag))['USD']['last']


def notify():
    playsound('sweep.wav')
    playsound('sweep.wav')
    playsound('sweep.wav')
