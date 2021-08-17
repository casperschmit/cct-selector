from numpy import log
from scrapy.exceptions import IgnoreRequest, CloseSpider
from twisted.internet import reactor

from scrapy.settings.default_settings import DOWNLOADER_MIDDLEWARES
from scrapy.spiders import CrawlSpider
from scrapy import signals
from pydispatch import dispatcher

from application import ROOT_DIR

import pickle
import re
import os


class ScrapeSpider(CrawlSpider):
    handle_httpstatus_list = [404]
    content = ""

    def __init__(self, name=None, store_dir='', start_urls=None, rules=None):
        super(ScrapeSpider, self).__init__(name, start_urls=start_urls, rules=rules)
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        # self.content = ""
        self.store_dir = store_dir
        self.stoprepetitionsrearg = re.compile('.*?\&(.*?\&)\1{1,}.*')
        self.stoprepetitionsreslash = re.compile('.*?\/(.*?\/)\1{1,}.*')

    def parse_item(self, response):
        text = "".join(response.css("::text").extract())
        self.content += text

        if self.stoprepetitionsrearg.match(response.url) != None or \
                self.stoprepetitionsreslash.match(response.url) != None:
            raise IgnoreRequest

    def spider_closed(self):
        dump_path = self.store_dir
        with open(self.store_dir, 'wb') as f:
            pickle.dump(self.content, f)
