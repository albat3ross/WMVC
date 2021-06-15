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


def request_general(url, request_type='GET', headers=None, is_gzipped=False, name_tag="", resp_form=False):
    if headers is None:
        headers = {}
    tic = time.perf_counter()
    try:
        request_message = urllib.request.Request(url=url, headers=headers, method=request_type)
        with urllib.request.urlopen(request_message, timeout=REQUEST_TIME_OUT) as response_message:
            if is_gzipped:
                response_message = zlib.decompress(response_message.read(), 16 + zlib.MAX_WBITS)
            if resp_form:
                return response_message
            soup = BeautifulSoup(response_message, features="html.parser")
    except Exception as err:
        if type(err) == timeout:
            logging.error(f'{request_type} url timeout: [{name_tag}] {err}')
        else:
            logging.error(f'{request_type} url failed: [{name_tag}] {err}')
        return None
    toc = time.perf_counter()
    logging.debug(f'Request {request_type}... [url: {url}]. Time taken:\t{toc - tic:0.4f}s')
    return soup


if __name__ == '__main__':
    from web_info import DEFAULT_HEADER
    print(request_general('https://github.com/', headers=DEFAULT_HEADER, is_gzipped=True).prettify())
