# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 22:33:36 2021

@author: zhouh
"""
import zlib
import time
import urllib.parse
import urllib.request
import logging
from socket import timeout

from bs4 import BeautifulSoup

REQUEST_TIME_OUT = 15


def mock_data(info):
    data = {} if not info.data else info.data
    return bytes(urllib.parse.urlencode(data), encoding='utf-8')


def mock_header(info):
    header = dict(info.header)
    if info.data:
        for entry in info.data.keys():
            header[entry] = info.data[entry]
    return header


def request_general(info):
    request_type = info.request
    tic = time.perf_counter()
    try:
        request_message = urllib.request.Request(url=info.url, data=mock_data(info), headers=mock_header(info),
                                                 method=request_type)
        with urllib.request.urlopen(request_message, timeout=REQUEST_TIME_OUT) as response_message:
            if info.is_gzipped:
                response_message = zlib.decompress(response_message.read(), 16 + zlib.MAX_WBITS)
            soup = BeautifulSoup(response_message, features="html.parser")
    except Exception as err:
        if type(err) == timeout:
            logging.warning(f'{request_type} url timeout: [{info.url}] {err}')
        else:
            logging.error(f'{request_type} url failed: [{info.url}] {err}')
    toc = time.perf_counter()
    logging.debug(f'Request {request_type}... [url: {info.url}]. Time taken:\t{toc - tic:0.4f}s')
    return soup

