import re
import pandas as pd
import numpy as np
import random
from collections import Counter

class ng_models(object):


    def __init__(self, n: int, corpus: str ):

        assert isinstance(n, int)
        assert isinstance(corpus , str)
        assert n>0
        assert len(corpus)>0

        self.n = min(n,5)
        self.get_specials(self)

        self.corpus = self.process_text(self, corpus)


        self.model_dict = self.create_model(self)
        self.first_words = self.get_first_words(self)

        self.V = len(set(self.corpus.split()))-1

    @staticmethod
    def get_specials(self):
        '''
        Creates sets od special symbols (</s> <s>) that will be used for marking beginings and endings of the sentences.
        Their length depends on 'n' parameter.
        '''    
        self.replacement = ' </s> <s> '
        self.sent_start = '<s> '

        for _ in range(self.n-1):
            self.replacement += '<s> '
            self.sent_start += '<s> '

    @staticmethod
    def process_text(self, t):
        '''
        Quick preprocessing of the text. Removes some special symbols and adds special strings calculated by 'get_specials' method.
        '''
        t = self.sent_start + t
        t = re.sub(r'\s+',' ',t.lower())
        t = re.sub(r'\ r\.',' r',t)
        t = re.sub(',','',t)
        
        t = re.sub(r'[!?.] ',self.replacement , t)
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
        '''
        Crates the list of words that occur in the first position in at leas one sentence in the corpus.
        '''
        assert hasattr(self, 'model_dict')
       
        first_words = re.findall(rf'{self.sent_start}([^ ]+)', self.corpus)
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
        
        speech = re.sub('<s>', '', ' '.join(speech))
        speech = re.sub('</s>', '', speech)
        speech = re.sub(r'\s+',' ',speech)

        return speech


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


    def mprob_sent(self, start_word: str ='', max_len: int =30):
        """
        Generates most probable sentence for given model that starts with 'start_word'. 
        If 'start_word' is empty searches for most common word among the 'first_words' of the model.

        start_word: str
        max_len: int
        """
        stopper = 0
        try:
            sentence = self.sent_start + start_word.lower()
            new_word = Counter(self.model_dict[sentence.split()[-self.n:][0]]).most_common(1)[0][0]
            if new_word=='</s>':
                sentence = re.sub('<s>','', sentence)
                sentence = re.sub(r'\s+',' ', sentence)
                return sentence.strip().capitalize() + '.'
            else:
                sentence += ' '+new_word
        except:
            print('Zaczynam od najpopularniejszego początku zdania w modelu...')
            sentence = self.sent_start + ' '+ Counter(self.first_words).most_common(1)[0][0]

        for _ in range(max_len):
            s_part = sentence.split()[-self.n:]
            if Counter(self.model_dict[' '.join(s_part)]).most_common(1)[0][0]=='</s>':
                break
            else:
                new_word = Counter(self.model_dict[' '.join(s_part)]).most_common(1)[0][0]
                if new_word in sentence.split():
                    try:
                        new_word = Counter(self.model_dict[' '.join(s_part)]).most_common(2)[1][0]
                        if new_word=='</s>':
                            break
                    except:
                        pass
                    stopper+=1
                    if stopper>2:
                        break

                sentence += ' ' + new_word

        sentence = re.sub('<s>','', sentence)
        sentence = re.sub(r'\s+',' ', sentence)
        sentence = sentence.strip().capitalize() + '.'

        return sentence
