"""
WMVC main class
Author: Han Zhou

"""
import logging
import threading
import time

from util import url_requester, utils

VERSION = 0.1

# TODO: adjust the running param here
# run time for the script in sec
DEFAULT_RUN_TIME = 60 * 1 * 1
# wait time between each inspection in sec, cannot be too short
WAIT_TIME = 20


class VCMonitor:
    """Video Card Monitor class."""
    def __init__(self, runtime=DEFAULT_RUN_TIME, logger_file_name=None, web_list=None):
        self.runtime = runtime
        self.web_list = utils.get_web_list() if web_list is None else web_list
        utils.init_logger(logger_file_name)
        logging.info(f'Start initializing gpu_getter ver.{VERSION}')

    def run(self):
        start_time = time.perf_counter()
        curr_time = time.perf_counter()
        web_list_len = len(self.web_list.keys())
        web_list_str = "\n\t" + "\n\t".join(self.web_list.keys())

        if WAIT_TIME < url_requester.REQUEST_TIME_OUT:
            raise RuntimeError('Wait time cannot be less than request timeout.')

        logging.info(f'Start running gpu_getter...\nMonitoring list length: {web_list_len}\n'
                     f'Monitoring list:[{web_list_str} \n]\nWaiting time for each inspection: [{WAIT_TIME}s]\n')
        loop_cnt = 1

        while curr_time - start_time < self.runtime:
            curr_time = time.perf_counter()
            logging.info(f'LOOP {loop_cnt}')
            result_list = [None for i in range(web_list_len)]
            for index, web_name in enumerate(self.web_list.keys()):
                thread = threading.Thread(target=self.read_once, args=[web_name, result_list, index])
                thread.start()
            while None in result_list:
                time.sleep(1)
            if True in result_list:
                break
            rest_time = WAIT_TIME - (time.perf_counter() - curr_time)
            if rest_time > 0.0:
                time.sleep(rest_time)
            curr_time = time.perf_counter()
            loop_cnt += 1

        logging.info(f'gpu_getter finished running after {loop_cnt-1} loops.')

    def read_once(self, web_name, result=None, index=None):

        if web_name not in self.web_list.keys():
            logging.error(f"[{web_name}] This entry is not in the list.")
            raise NotImplementedError

        web_info = self.web_list[web_name]
        message = url_requester.request_general(web_info)
        find = utils.process_soup(message, web_info)
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
