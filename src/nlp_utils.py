import re
from constants import STOP_WORDS

def clean_sentence(s):
    return s.lower().replace(',', '').replace("|", "").replace("\"", "")\
        .replace("’", "").replace("'", "").replace(".", "")\
        .replace("…", "").replace("-", " ").replace("–", " ")\
        .replace("_", " ").replace("/", " ").replace("!", "")\
        .replace("(", "").replace(")", "")\
        .replace("®", "").replace("+", "")\
        .replace("&", "").replace("#", "")

def clean_word(w):
    w = clean_sentence(w)
    if len(w) <= 2 or (len(w) > 2 and w[-2:] == "ss"):
        return w
    else:
        return re.compile(r"s$").sub('', w)
    
def remove_stop_words(s):
    cleared = []
    for w in clean_sentence(s).split():
        word = clean_word(w)
        if word not in STOP_WORDS:
            cleared.append(word)
    return ' '.join(cleared)