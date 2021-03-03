"""Util functions for python"""
import csv
import logging
import re
from playsound import playsound
from colorlog import ColoredFormatter

from web_info import WebInfo


LOG_FORMAT_SIMPLE = '%(asctime)s %(levelname)s : %(message)s'
LOG_FORMAT_FULL = "%(log_color)s%(levelname)s%(reset)s | %(log_color)s%(message)s%(reset)s"


def init_logger(logger_file_name: str):
    if not logger_file_name:
        logger_file_name = DEFAULT_LOGGER_NAME
    logging.basicConfig(filename=logger_file_name,
                        filemode='w',
                        level=logging.INFO,
                        format=LOG_FORMAT_SIMPLE)
    formatter = ColoredFormatter(LOG_FORMAT_FULL)
    stream = logging.StreamHandler()
    stream.setLevel(logging.INFO)
    stream.setFormatter(formatter)
    logging.getLogger('').addHandler(stream)


def process_soup(soup, web_info):
    availabilityMessage = soup.find(web_info.trace_type, class_=re.compile(web_info.trace_tag))
    if not availabilityMessage:
        logging.error(f'Cannot trace availabilityMessage from tag {web_info.trace_tag}.')
        return
    if not availabilityMessage.text:
        logging.error('Cannot find text in availabilityMessage.')
        return
    # print(availabilityMessage.text)
    return availabilityMessage.text not in web_info.available_message


def get_web_list(web_list_str):
    web_list = {}
    with open(web_list_str) as web_list_csv:
        csv_reader = csv.reader(web_list_csv, delimiter=',')
        for row in csv_reader:
            if len(row) < 3 or row[0][0] == '#':
                continue
            web_list[row[1]] = WebInfo.GetWebInfo(row[2], row[0])
    return web_list


def notify():
    playsound('sweep.wav')
    playsound('sweep.wav')
    playsound('sweep.wav')
