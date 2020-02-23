import re
import pandas as pd
import numpy as np

class ng_models(object):


    def __init__(self, n: int, corpus: str ):

        assert isinstance(n, int)
        assert isinstance(corpus , str)
        assert n>0
        assert len(corpus)>0

        self.n = min(n,5)
        self.corpus = self.process_text(self, corpus)
     

        self.model_dict = self.create_model(self)
        self.first_words = self.get_first_words(self)


    @staticmethod
    def process_text(self, t):
        t = re.sub(r'\s+',' ',t)
        t = re.sub(r'\ r.',' r',t)
        t = re.sub(r'[!?.] ',' </s> <s> ',t.lower())
        return t
        
    @staticmethod
    def create_model(self) -> dict:
        words, words_model = list(), dict()

        words = self.corpus.split()
        for i in range(len(words) - self.n):
            speech_part = ' '.join(words[i:i + self.n])
            if speech_part not in words_model.keys():
                words_model[speech_part] = []
            words_model[speech_part].append(words[i + self.n])

        return words_model

    @staticmethod
    def get_first_words(self):
        assert hasattr(self, 'model_dict')

        first_words = [k.split()[1] for k in list(self.model_dict.keys()) if k.split()[0]=='<s>']
        return first_words