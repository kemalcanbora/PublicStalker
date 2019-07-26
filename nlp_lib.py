from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from collections import Counter
from settings import treebank_dict
import nltk



def treebank_convert(pos_tag_dict):
    return dict((treebank_dict[key], value) for (key, value) in pos_tag_dict.items())


class Analytics:
    def __init__(self):
        pass
    def tokenized_data(self, text):
        stop_words = set(stopwords.words("turkish"))
        tokenized_word = word_tokenize(text)
        filtered_sent = []
        for w in tokenized_word:
            if w not in stop_words:
                filtered_sent.append(w)

        return filtered_sent

    def stemmed_data(self,filtered_sent):
        stemmed_words = []
        tokenizer = RegexpTokenizer(r'\w+')
        for w in filtered_sent:
            if tokenizer.tokenize(w) != []:
                if len(w) > 2:  # rulebase for char string
                    stemmed_words.append(tokenizer.tokenize(w.lower()).pop())

        return stemmed_words

    def pos_tag_analiz(self, text_list):
        clean = []
        for item in text_list:
            if item is not None:
                clean.append(item)
        text = ' '.join(clean)
        filtered_sent = self.tokenized_data(text)
        stemmed_words = self.stemmed_data(filtered_sent)
        pos_tag = nltk.pos_tag(stemmed_words)
        count = Counter([j for i, j in pos_tag])
        result = treebank_convert(dict(count.most_common(20)))
        return {"treebank":result,
                "stemmed":dict(Counter(stemmed_words).most_common(20))}