import spacy
import re
from gensim.parsing.preprocessing import remove_stopwords, strip_multiple_whitespaces

# Also function used in search package
def split_content(content):
    sentence_structure = re.compile(r'([A-Z\xc4\xc5\xd6][^\.!?]*[\.!?])', re.M)
    sentences = sentence_structure.findall(content)
    return sentences


# Process content for search
def process_content(content, nlp):
    temp = strip_multiple_whitespaces(content)  # Strip \n \t and other whitespace chars
    temp = remove_stopwords(temp)  # Remove stop words: if, a, with etc.

    # Increase max length of nlp if text is too long. We do not need parser and ner for lemmatizing, so it's ok.
    if len(temp) > 1000000:
        nlp.max_length = len(temp) + 100
    doc = nlp(temp)  # Lemmatize words
    temp = " ".join([token.lemma_ for token in doc])
    return temp
