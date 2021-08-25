import re
import pandas as pd
import pycountry

from pathlib import Path

from urllib.parse import urlparse
from urllib import request

from gensim.models import Word2Vec, KeyedVectors

from scrapy.crawler import CrawlerProcess
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging

from search.build.spider import ScrapeSpider
from search.build.train import read_knowledge_base, train_model
from search.query.query import perform_search
from search.query.index import clean_index

from whoosh.index import open_dir

from twisted.internet import reactor, defer

from flaskdss import ROOT_DIR


def start_crawl(filename, path):
    configure_logging()
    runner = CrawlerRunner()

    @defer.inlineCallbacks
    def crawl():
        for i in interpret_df(filename, path, runner):
            yield i
        if reactor.running:
            reactor.stop()

    crawl()
    if len(runner.crawlers) > 0:
        reactor.run()  # the script will block here until the last crawl call is finished


def crawl_web_docs(name, url, base_url=None):
    if base_url is None:
        base_url = url

    process = CrawlerProcess()
    process.crawl(ScrapeSpider, name=name, start_urls=[url],
                  rules=[Rule(LinkExtractor(allow=base_url), callback='parse_item', follow=True)])
    process.start(stop_after_crawl=True)
    reactor.stop()


def download_pdf(download_url, location):
    headers = {
        'User-Agent': "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Mobile Safari/537.36"}
    req = request.Request(url=download_url, headers=headers)
    try:
        with request.urlopen(req) as response:
            file = open(location + ".pdf", 'wb')
            file.write(response.read())
            file.close()
    except:
        print('error')
        pass


def get_base_url(url):
    parsed_url = urlparse(url)
    split_path = parsed_url.path.split("/")
    first_path_element = ''
    if len(split_path) >= 2:
        first_path_element = split_path[1]
        if len(split_path) >= 3 and pycountry.languages.get(alpha_2=split_path[2]):
            first_path_element += ('/' + str(split_path[2]))
    base_url = parsed_url.scheme + '://' + parsed_url.netloc + '/' + str(first_path_element)
    return str(base_url)


def interpret_df(df, path, runner):
    pdf = re.compile('.*\.pdf$')
    for index, row in df.iterrows():  # df.iloc[1:].iterrows():
        name = row[1]
        docs = row.docs
        wp = row.whitepaper

        # Make directory with CCT name
        location = path + "/" + name
        Path(location).mkdir(parents=True, exist_ok=True)

        # Handle docs
        if docs is not None and pdf.match(docs):
            download_pdf(docs, location + '/' + name + '_docs')
        elif docs is not None:
            base_url = get_base_url(docs)
            yield runner.crawl(ScrapeSpider, name=name, store_dir=location + "/" + name + ".pkl", start_urls=[docs],
                               rules=[Rule(LinkExtractor(allow=base_url), callback='parse_item', follow=True)])
        else:
            yield 1

        # Handle whitepapers
        if wp is not None and pdf.match(wp):
            download_pdf(wp, location + '/' + name + '_wp')
        elif wp is not None:
            yield runner.crawl(ScrapeSpider, name=name, store_dir=location + "/" + name + "_wp.pkl", start_urls=[wp],
                               rules=[Rule(LinkExtractor(allow=wp), callback='parse_item', follow=False)])
        else:
            yield 1
    yield 1


def get_attribute_results(results, filename):
    attribute_results = []
    df = pd.read_excel(filename)

    for result in results:
        relevancy = str(round(results[result], 2))
        if not df.loc[df['Name'] == result].empty:
            row = df.loc[df['Name'] == result]
            dev_support = row['Developer support'].tolist()[0]
            type = row['Type'].tolist()[0]
            defi_focus = row['DeFi focus'].tolist()[0]
            attribute_results.append([result, dev_support, relevancy, type, defi_focus])
        else:
            attribute_results.append([result, 'N/A', relevancy, 'N/A', 'N/A'])

    return attribute_results


def keyword_search_handler(df, kb_path, search_limit, re_calibrate, input_content):
    model_name = ROOT_DIR + "/search/test_model2"
    kb_path = ROOT_DIR + "/" + kb_path
    index_path = ROOT_DIR + "/search/index"

    if re_calibrate or not Path(model_name).exists():
        # Crawl from input excel file
        print("--------------------- CRAWL -----------------------")
        start_crawl(df, kb_path)
        print("--------------------- READ KB -----------------------")
        kb = read_knowledge_base(kb_path)
        print("--------------------- TRAIN MODEL -----------------------")
        model = train_model(kb)
        model.save(model_name)
        print("--------------------- CLEAN INDEX -----------------------")
        ix = clean_index(index_path, kb_path)
    else:
        ix = open_dir(index_path)
        model = Word2Vec.load(model_name)

    results = perform_search(input_content, ix, model, alternative_keyword_depth=10, search_limit=search_limit)
    return results
