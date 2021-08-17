import pickle
from whoosh.fields import Schema, TEXT, ID
from whoosh.index import create_in
from tika import parser
import os
import re
from search.util import process_content
import spacy

nlp = spacy.load('en_core_web_md', disable=['parser', 'ner'])


def clean_index(index_path, kb_path):
    schema = Schema(path=ID(unique=True, stored=True), content=TEXT)

    if not os.path.exists(index_path):
        os.mkdir(index_path)
    ix = create_in(index_path, schema)

    writer = ix.writer()
    pdf = re.compile('.*\.pdf$')
    pkl = re.compile('.*\.pkl$')

    for dir in os.listdir(kb_path):
        content = ""
        currentdir = kb_path + '/' + dir
        for filename in os.listdir(currentdir):
            path = currentdir + '/' + filename
            if pdf.match(path):
                content += read_pdf(path)
            elif pkl.match(path):
                content += read_pickle(path)
            else:
                # TODO possibly implement more types
                pass
        writer.add_document(path=dir, content=content)
    writer.commit()
    return ix


def read_pickle(path):
    with open(path, 'rb') as f:
        content = pickle.load(f)
    return process_content(content, nlp)


def read_pdf(path):
    raw = parser.from_file(path)
    content = raw['content']
    return process_content(content, nlp)

