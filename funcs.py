import re
import pandas as pd
import stanza


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
        t = re.sub(r'(\d+[, ]+)*(i )*\d+ punkt porządku dziennego:', '', t)
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
        t = re.sub(r'\s+', ' ', t)
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
        return re.sub(r'\[COM\(2005\)0119 - C6-0099/2005 - 2005/0043\(COD\)\]', ' ', r)
    else:
        return r


def print_topics(topic_list):
    '''Prints topics and characteristic words for them as a table'''
    topic_df = pd.DataFrame()
    for topic in topic_list:
        topic_df['Topic ' + str(topic[0])] = pd.Series(topic[1].split(' + ')).apply(lambda x : re.sub(r'[\d\.\*\"\']', '', x))
    return topic_df
