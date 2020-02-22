import re
import pandas as pd

def name_finder(t):
    """ Finds name of the speech author"""
    
    try:
        name = re.findall(r'[Pp]oseł ([\w -\.]+):',t)[0]
    except:
        try:
            name = re.findall(r'[Pp]oseł ([\w -\.]+) Panie',t)[0]
        except:
            return None
    return name
    

def rem_head(t):
    """Removes header regarding the number of day order"""
    
    try:
        t = re.sub('(\d+[, ]+)*(i )*\d+ punkt porządku dziennego:', '', t)
    except:
        return t
    return t

#print(name_finder('ruk nr 1864). Poseł Wiesław ss kkkk Piątkowski Sza'))

def clear_text(t):
    """Removes special signs

    :type t: basestring
    """
    try:
        t = re.sub('[\n\r\t]', ' ', t)
    except:
        return None

    try:
        t = re.sub('\s+', ' ', t)
    except:
        return t
    return t

def rem_title(title, raw_text):
    """Removes title of the speech from its text

    :type title: string
    :type raw_text: string"""
    if not pd.isnull(title) and not pd.isnull(raw_text) and not raw_text is None:
        try:
            re.sub(title, '', raw_text)
            return re.sub(title, '', raw_text)
        except:
            return raw_text
    else:
        return raw_text

def rem_nasty(r):
    """Jednorazowa korekta"""
    if not r is None and not pd.isnull(r):
        return re.sub('\[COM\(2005\)0119 - C6-0099/2005 - 2005/0043\(COD\)\]', ' ', r)
    else:
        return r


def perplexity(sentence, model):
    """Calculated perplexity with 1-add smoothing

    sentence: string
    model: dictionary with n-grams"""


def model_ng(corpus: str, n: int = 1):
    """Builds n-gram model on given corpora"""
    assert len(corpus) > 0, 'Brak danych do budowy modelu.'

    words, words_model = list(), dict()

    words = corpus.split()
    for i in range(len(words) - n):
        speech_part = ' '.join(words[i:i + n])
        if speech_part not in words_model.keys():
            words_model[speech_part] = []
        words_model[speech_part].append(words[i + n])

    return words_model