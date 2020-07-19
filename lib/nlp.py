import spacy
import numpy as np
from typing import List
from sklearn.feature_extraction.text import TfidfVectorizer


class NLP(object):
    def __init__(self, model="en_core_web_sm"):
        self.nlp = spacy.load(model)

    def annotate(self, text: str):
        return self.nlp(text)

    def tfidf_feature_top(self, docs: List[str], n=10):
        bow = []
        for text in docs:
            doc = self.nlp(text)
            words = ' '.join([token.lemma_ for token in doc if token.pos != 'PUNCT' and not token.is_stop])
            bow.append(words)

        corpus = np.array(bow)
        tfidf = TfidfVectorizer()
        x = tfidf.fit_transform(corpus)
        result = x.toarray()
        feature_names = np.array(tfidf.get_feature_names())
        index = result.argsort(axis=1)[:, ::-1]
        feature_words = [feature_names[row[:n]] for row in index]

        return feature_words
