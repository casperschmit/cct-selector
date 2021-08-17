from whoosh.qparser import QueryParser

from search.query import nlp
from search.util import split_content, process_content
from gensim import utils


def get_alternatives_string(word, akd, model):
    try:
        alternatives = model.wv.most_similar(word)
    except KeyError:
        return "(" + word + ")"

    result = "(" + word
    akd -= 1

    for alternative in alternatives:
        if akd <= 0:
            break
        result += (" OR " + alternative[0])  # Get first element of tuple
        akd -= 1
        # if i < (akd - 1) and alternative[0] != alternatives[-1][0]:
        #     result += " OR "

    result += ")"
    return result


def construct_query(sentence, akd, model):
    query_string = ""
    for word in sentence:
        alternatives = get_alternatives_string(word, akd, model)
        query_string += alternatives
        if word != sentence[-1]:
            query_string += " AND "
    return query_string


def get_list_avg(results):
    for result in results:
        avg = sum(results[result]) / len(results[result])
        results[result] = avg
    return results


def sort_dict(avg_results):
    return dict(sorted(avg_results.items(), key=lambda item: item[1], reverse=True))


def perform_search(content, index, model, alternative_keyword_depth=3, search_limit=5):
    sentences = split_content(content)
    if not sentences:
        sentences = [content]
    results = {}

    for sentence in sentences:
        sentence = utils.simple_preprocess(process_content(sentence, nlp))
        query = construct_query(sentence, alternative_keyword_depth, model)
        results.update(search(index, query, search_limit, results))

    avg_results = get_list_avg(results)
    results = sort_dict(avg_results)
    return results


def store_results(results, result_dict):
    for result in results:
        print(result['path'] + " with score " + str(result.score))
        if not result['path'] in result_dict.keys():
            result_dict[result['path']] = [result.score]
        else:
            result_dict[result['path']].append(result.score)
    return result_dict


def search(ix, query, search_limit, result_dict):
    parser = QueryParser("content", ix.schema)
    myquery = parser.parse(query)
    results = None
    with ix.searcher() as searcher:
        results = searcher.search(myquery, limit=search_limit)
        result_dict = store_results(results, result_dict)
    return result_dict
