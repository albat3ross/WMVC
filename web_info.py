"""WebInfo class"""
from typing import Optional

from video_card_type import VideoCard

DEFAULT_HEADER = {
    'method': 'GET',
    'scheme': 'https',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'cache-control': 'max-age=0',

    'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36",
}


def getBestBuy(url):

    HEADER_BESTBUY = dict(DEFAULT_HEADER)
    HEADER_BESTBUY['authority'] = 'www.bestbuy.ca'
    HEADER_BESTBUY['path'] = "//en-ca//category//video-cards//20397"

    BESTBUY_TRACETAG = 'availabilityMessage*'
    BESTBUY_AVAILABLE_MESSAGE = ['Coming soon', 'Sold out online']

    return WebInfo(url=url,
                   header=HEADER_BESTBUY,
                   is_gzipped=True,
                   trace_tag=BESTBUY_TRACETAG,
                   ava_msg=BESTBUY_AVAILABLE_MESSAGE,
                   trace_type='span',
                   )


def getNewEgg(url):

    HEADER_NEWEGG = dict(DEFAULT_HEADER)
    HEADER_NEWEGG['authority'] = 'www.newegg.ca'
    HEADER_NEWEGG['path'] = "/p/pl?N=100007708&d=3070"

    NEWEGG_TRACETAG = 'product-inventory'
    NEWEGG_AVAILABLE_MESSAGE = [' OUT OF STOCK.']

    return WebInfo(url=url,
                   header=HEADER_NEWEGG,
                   is_gzipped=True,
                   trace_tag=NEWEGG_TRACETAG,
                   ava_msg=NEWEGG_AVAILABLE_MESSAGE,
                   )


def getNewEggCombo(url):
    web_info = getNewEgg(url)
    web_info.trace_tag = 'note'
    web_info.trace_type = 'p'
    web_info.available_message = ['OUT OF STOCK']
    return web_info


def getPCCanada(url):
    HEADER_PCCANADA = dict(DEFAULT_HEADER)
    HEADER_PCCANADA['authority'] = 'www.pc-canada.com'
    HEADER_PCCANADA['path'] = url.split('.com')[1]

    PCCANADA_TRACETAG = 'text-theme-shipping'
    PCCANADA_AVAILABLE_MESSAGE = [' On Backorder']

    return WebInfo(url=url,
                   header=HEADER_PCCANADA,
                   is_gzipped=True,
                   trace_tag=PCCANADA_TRACETAG,
                   trace_type='span',
                   ava_msg=PCCANADA_AVAILABLE_MESSAGE)


class WebInfo:
    """WebInfo class"""
    url: str
    header: dict
    data: dict
    request: str
    is_gzipped: bool
    trace_tag: str
    available_message: list
    trace_type: str
    video_card: Optional[VideoCard]

    def __init__(self, url, header=None, data=None, request='GET',
                 is_gzipped=False, trace_tag='', ava_msg=None, trace_type='div'):
        if ava_msg is None:
            ava_msg = []
        if header is None:
            header = DEFAULT_HEADER
        if data is None:
            data = {}
        self.url = url
        self.header = header
        self.data = data
        self.request = request
        self.is_gzipped = is_gzipped
        self.trace_tag = trace_tag
        self.available_message = ava_msg
        self.trace_type = trace_type
        self.video_card = None

    @staticmethod
    def GetWebInfo(url, web_type):
        if web_type == 'BestBuy':
            return getBestBuy(url)
        elif web_type == 'NewEgg':
            return getNewEgg(url)
        elif web_type == 'NewEgg_Combo':
            return getNewEggCombo(url)
        elif web_type == 'PCCanada':
            return getPCCanada(url)
        else:
            raise NotImplementedError


if __name__ == '__main__':
    wb = WebInfo.GetWebInfo('https://www.pc-canada.com/item/TUF-GTX1650S-O4G-GAMING', 'PCCanada')
    print('end')
