import re
import pandas as pd

def name_finder(t):
    ''' Wyszukuje i zwraca imie i nazwisko przemawiajacego posla'''
    
    try:
        name = re.findall(r'[Pp]oseł ([\w -\.]+):',t)[0]
    except:
        try:
            name = re.findall(r'[Pp]oseł ([\w -\.]+) Panie',t)[0]
        except:
            return None
    return name
    

def rem_head(t):
    """Kasuje naglowek dotyczacy numeru porządku dziennego"""
    
    try:
        t = re.sub('(\d+[, ]+)*(i )*\d+ punkt porządku dziennego:', '', t)
    except:
        return t
    return t

#print(name_finder('ruk nr 1864). Poseł Wiesław ss kkkk Piątkowski Sza'))

def clear_text(t):
    """Czysci znaki specjalne
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
    """Usuwa fragment, ktory jest tytulem przemowienia
    :type title: string
    :type raw_text: string"""
    if not pd.isnull(title) and not raw_text is None:
        print(title)
        res = re.sub(title, '', raw_text)
        return res
    else:
        return raw_text

def rem_nasty(r):
    """Jednorazowa korekta"""
    if not r is None and not pd.isnull(r):
        return re.sub('\[COM(2005)0119 - C6-0099/2005 - 2005/0043(COD)\]', ' ', r)
    else:
        return r