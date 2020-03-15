import re
import pandas as pd
import numpy as np
import random

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

        self.V = len(set(self.corpus.split()))-1


    @staticmethod
    def process_text(self, t):
        t = '<s> ' + t
        t = re.sub(r'\s+',' ',t.lower())
        t = re.sub(r'\ r\.',' r',t)
        t = re.sub(',','',t)
        
        replacement = ' </s> <s> '
        for _ in range(self.n-1):
            replacement += '<s> '
            t = '<s> ' + t
        t = re.sub(r'[!?.] ',replacement , t)

        t += ' </s>'

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
        sent_start = '<s>'
        for _ in range(self.n-1):
            sent_start = sent_start + ' <s>'
        first_words = re.findall(rf'{sent_start} ([^ ]+)', self.corpus)
        return first_words

    def generate(self, steps: int = 60, max_sent: int = 20):
        """
        Generates text of length 'steps' sentences with sentences of maximum length 'max_sent'.

        steps: int
        max_sent: int
        """
        
        speech = list()
        
        while len(speech)<steps:
            sentence=''
            
            w1 = self.first_words[random.randrange(len(self.first_words))]

            try:
                first_keys = [k for k in list(self.model_dict.keys()) if k.split()[0]==w1]
            except:
                first_keys = [self.model_dict[w1]]
            
            sent_start  = first_keys[random.randrange(len(first_keys))]

            words = sent_start
            sentence = sent_start.capitalize()
            sent_len=2
            ifend=0
            
            while sent_len<max_sent and ifend==0:
                try:
                    possibilities = self.model_dict[words]
                    next_item = possibilities[random.randrange(len(possibilities))]
                except:
                    next_item = '</s>'
                
                if next_item == '</s>':
                    ifend = 1
                    speech.append(sentence+'.')
                else:
                    sentence += ' ' + next_item
                    words = ' '.join(sentence.split()[-self.n:])
                    sent_len+=1
                
                if ifend==0 and sent_len>=max_sent:
                    speech.append(sentence+'.')
                
        return ' '.join(speech)

    def perplexity(self, sentence):
        """
        Calculates the perplexity of the sentence. High perplexity means that model is rather surprised with the sentence.

        sentence: str
        """
        N = len(sentence.split())
        sentence = self.process_text(self, sentence)
 
        sentence = sentence.split()

        p=1
        for i in range(N+1):
            try:
                dic_frag = self.model_dict[' '.join(sentence[i:i+self.n])]
                denom = len(dic_frag)+self.V
                enum= len([v for v in dic_frag if v == sentence[i+self.n]])+1
                p = p*enum/denom
            except:
                p=p*(1/(1+self.V))
        return p**(-1/N)