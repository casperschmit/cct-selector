from search.build import nlp
from search.util import process_content, split_content
from tika import parser
from gensim import utils
from gensim.models import Word2Vec
import re
import os
import pickle


def read_knowledge_base(dirpath):
    knowledge_base = []
    pdf = re.compile('.*\.pdf$')
    pkl = re.compile('.*\.pkl$')
    for root, dirs, files in os.walk(dirpath):
        for name in files:
            path = root + '/' + name
            if pdf.match(path):
                knowledge_base += read_pdf(path)
            elif pkl.match(path):
                knowledge_base += read_pickle(path)
            else:
                print("Else in read_knowledge_base")
            #             TODO implement other file types / sources
    return knowledge_base


def process_sentences(sentences):
    for i in range(len(sentences)):
        sentences[i] = utils.simple_preprocess(process_content(sentences[i], nlp))
    return sentences


def read_pickle(path):
    with open(path, 'rb') as f:
        content = pickle.load(f)
    return process_sentences(split_content(content))


def read_pdf(path):
    raw = parser.from_file(path)
    content = raw['content']
    return process_sentences(split_content(content))


def train_model(content):
    model = Word2Vec(sentences=content, epochs=10)
    return model
