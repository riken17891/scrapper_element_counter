from utils import logger, read_url, sort_dict_and_get_top_elements
from HTMLParser import HTMLParser
from collections import OrderedDict

import json
import sys


class CustomHtmlParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.elements = dict()
        self.total_elements = 0

    # feed html and collect each element and it's count
    def feed_and_collect(self, html):
        self.feed(data=html)

    # pull top frequently occurred elements and their counts
    def top_elements(self, number=5):
        return OrderedDict(sort_dict_and_get_top_elements(data_dict=self.elements, number=number))

    # get start tag and save to dict along with count for each tag
    def handle_starttag(self, tag, attrs):
        logger.debug("start tag : {}".format(tag))

        self.total_elements += 1

        if tag in self.elements:
            self.elements[tag] += 1
        else:
            self.elements[tag] = 1


def scrape_and_collect(url):
    logger.info("started scrapping : {}".format(url))

    # read url and get response body
    html = read_url(url=url)
    logger.debug("page content : \n {}".format(html))

    # check if response is not blank, if blank then no need to process further
    if html == "":
        logger.error("empty response from URL, please provide valid URL")
        return dict()

    # initialize HtmlParser object
    parser = CustomHtmlParser()
    # feed html and collect elements
    parser.feed_and_collect(html=html)

    # set result as dictionary
    result = dict()
    result["total_elements"] = parser.total_elements
    result["top_elements"] = parser.top_elements(number=5)

    return result


if __name__ == '__main__':
    # try and see of valid URL is provided if yes then continue processing else return with error
    try:
        final = scrape_and_collect(url=sys.argv[1])

        # dump result dictionary to console and log file
        logger.info("result: \n{}".format(json.dumps(final, indent=2)))

    except IndexError as e:
        logger.error("please provide valid URL as a first argument while running a script")
