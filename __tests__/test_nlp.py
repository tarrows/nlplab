import unittest

from lib import NLP


class TestNLP(unittest.TestCase):
    def setUp(self):
        self.nlp = NLP()

    def test_topWords_itWorks(self):
        docs = [
            "This is an apple.",
            "These are cute dogs and cats.",
            "Apple is looking at buying U.K. startup for $1 billion"
        ]
        top_n = self.nlp.tfidf_feature_top(docs, n=3)
        self.assertTrue(all([len(words) == 3 and all([isinstance(word, str) for word in words]) for words in top_n]))


if __name__ == "__main__":
    unittest.main()
