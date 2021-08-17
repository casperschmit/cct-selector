import scrapy
from pydispatch import dispatcher
from scrapy import signals
import pickle
import pathlib


class GitSpider(scrapy.Spider):
    name = "gitspider"
    allowed_domains = ['github.com']

    def __init__(self, name=None, store_dir='', start_urls=None):
        super(GitSpider, self).__init__(name, start_urls=start_urls)
        self.content = []

    def parse(self, response, **kwargs):
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        web_page = response.xpath('/html/body/div[4]/main/div/header/div[1]/div/div[2]/div[2]/ul/li[2]/a')
        email = response.xpath('/html/body/div[4]/main/div/header/div[1]/div/div[2]/div[2]/ul/li[3]/a')

        if web_page is not None and email is not None:
            web_page = 1
            email = 1
        elif email is not None and web_page is None:
            email = 1
            web_page = 0
        elif web_page is not None and email is None:
            email = 0
            web_page = 1
        else:
            email = 0
            web_page = 0

        self.content = [web_page, email]

    def spider_closed(self):
        dump_path = str(pathlib.Path(__file__).parent.resolve()) + "/dev_supp.pkl"
        with open(dump_path, 'wb') as f:
            pickle.dump(list(self.content), f)
