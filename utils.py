import urllib2 as ul
import logging
import operator

logging.basicConfig(level=logging.INFO, handlers=[
        logging.FileHandler("scrapper.log"),
        logging.StreamHandler()
    ])
logger = logging.getLogger(__name__)


def read_url(url):

    if url is None:
        return ""

    try:
        # initiate url get request
        request = ul.Request(url=url)
        # open url and get response
        response = ul.urlopen(request)
        # read response body and return
        return response.read()
    except ul.HTTPError as e:
        logger.error("Error while reading url : {}".format(e))

    return ""


def sort_dict_and_get_top_elements(data_dict, number=5, descending=True):
    if data_dict is None:
        return None
    # sort dictionary by values and return list of tuples with top elements requested based on number value
    return sorted(data_dict.items(), key=operator.itemgetter(1), reverse=descending)[:number]
