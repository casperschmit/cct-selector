from search.build.train import read_knowledge_base, train_model
from search.query.query import perform_search
from search.query.index import clean_index
from whoosh.index import open_dir
from search.search import get_attribute_results, keyword_search_handler
from analysis.analysis import compute_attributes

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Crawl from input excel file
    # start_crawl('kb-input-test.xlsx', 'kb3')

    # Read crawled pages and pdfs
    # kb = read_knowledge_base("kb2")

    # Train and save model
    # model = train_model(kb)
    # model.save("test_model2")

    # model = Word2Vec.load("test_model")
    # alternatives = model.wv.most_similar('blockchain')
    # print(alternatives)
    # ix = clean_index("kb2")

    # ix = open_dir("search/index")
    # content = "I would like to create a blockchain to link two systems such as Bitcoin and Ethereum." \
    #           "Also, security, and speed is very important."
    content = "As a blockchain developer, I would like to link two systems together using ethereum and bitcoin. " \
              "In an ecosystem using the substrate network."
    # results = perform_search(content, ix, "search/test_model2", alternative_keyword_depth=3, search_limit=5)

    # results = keyword_search_handler("search/kb-input.xlsx", "search/kb3", 10, False, content)
    # print(get_attribute_results(results, "search/attributes.xlsx"))
    compute_attributes()
