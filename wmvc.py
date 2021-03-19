"""
WMVC main class
Author: Han Zhou

"""
import datetime
import logging
import threading
import time

from util import url_requester, utils
from util.utils import get_latest_crypto_price

VERSION = 0.1

# TODO: adjust the running param here
# run time for the script in sec
DEFAULT_RUN_TIME = 60 * 60 * 4
# wait time between each inspection in sec, cannot be too short
WAIT_TIME = 20
# monitor list file name
DEFAULT_LIST_STR = 'web_list.csv'
# logger file name
DEFAULT_LOGGER_NAME = 'runlog.log'


class VCMonitor:
    """Video Card Monitor class."""
    def __init__(self, runtime=None, logger_file_name=None):

        if runtime is None:
            runtime = DEFAULT_RUN_TIME

        if logger_file_name is None:
            logger_file_name = DEFAULT_LOGGER_NAME

        self.runtime = runtime
        self.web_list = utils.get_web_list(DEFAULT_LIST_STR)
        utils.init_logger(logger_file_name)
        logging.info(f'Start initializing WMVC monitor [ver {VERSION}]')
        logging.info(f'Current time is {datetime.datetime.now().strftime("%H:%M:%S")}, the bitcoin price is [{get_latest_crypto_price()}]')
        logging.info(f'Preset runtime:       [{self.runtime // 3600}] hour | [{(self.runtime % 3600)//60}] minute | [{self.runtime %60}] second')
        logging.info(f'Monitor list source:  [{DEFAULT_LIST_STR}].')
        logging.info(f'Log file saving as:   [{logger_file_name}].')

    def run(self):
        start_time = time.perf_counter()
        curr_time = time.perf_counter()
        web_list_len = len(self.web_list.keys())
        web_list_str = "\n\t" + "\n\t".join(self.web_list.keys())

        if WAIT_TIME < url_requester.REQUEST_TIME_OUT:
            raise RuntimeError('Wait time cannot be less than request timeout.')

        logging.info(f'Start running WMVC monitor...\nMonitoring list length: {web_list_len}\n'
                     f'Monitoring list:[{web_list_str} \n]\nWaiting time for each inspection: [{WAIT_TIME}s]\n')
        loop_cnt = 0

        while curr_time - start_time < self.runtime:
            curr_time = time.perf_counter()
            if loop_cnt == 0:
                logging.info(f'Checking stock...')
            else:
                logging.info(f'Inspection {loop_cnt} started...')
            result_list = [None for i in range(web_list_len)]
            for index, web_name in enumerate(self.web_list.keys()):
                thread = threading.Thread(target=self.read_once, args=[web_name, result_list, index])
                thread.start()
            while None in result_list:
                time.sleep(1)

            if True in result_list:
                break
            elif loop_cnt == 0:
                logging.info('All monitored items are currently unavailable, start periodic monitoring program...')

            rest_time = WAIT_TIME - (time.perf_counter() - curr_time)
            if rest_time > 0.0:
                time.sleep(rest_time)
            curr_time = time.perf_counter()
            loop_cnt += 1
        logging.info(f'WMVC monitor finished running after {loop_cnt} loops.')

    def read_once(self, web_name, result=None, index=None):

        if web_name not in self.web_list.keys():
            logging.error(f"[{web_name}] This entry is not in the list.")
            raise NotImplementedError

        web_info = self.web_list[web_name]
        message = url_requester.request_general(url=web_info.url,
                                                request_type=web_info.request,
                                                headers=web_info.header,
                                                name_tag=web_name,
                                                is_gzipped=web_info.is_gzipped)
        find = utils.process_soup(message, web_info) if message else False
        status = 'In STOCK' if find else 'OUT OF STOCK'

        logging.debug(f'[{web_name}] | Status: {status}')

        if find:
            logging.warning(f'Found card stock for [{web_name}], url: {web_info.url}')
            utils.notify()

        if result is not None and index is not None:
            result[index] = find

        return find


if __name__ == '__main__':
    VCMonitor().run()
