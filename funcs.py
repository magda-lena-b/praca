import re

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
    t = re.sub('[\n\r\t]', ' ', t)
    t = re.sub('\s+', ' ', t)
    return t