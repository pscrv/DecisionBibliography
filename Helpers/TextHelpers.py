import re

def countwords(text):
   return len(re.findall(r"\b['\w]+\b", text))

def countwordpairs(text):
    return countwords(text) - 1

def countstringoccurences(needle, haystack):
    return sum(1 for _ in re.finditer(r'%s' % re.escape(needle), haystack))

def countwordoccurences(needle, haystack):
    return sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(needle), haystack))

def countstringoccurencesinword(needle, haystack):
    return sum(1 for _ in re.finditer(r"\b(['\w]*)?%s(['\w]*)?\b" % re.escape(needle), haystack))

def countstringpairsinwords(needle1, needle2, distance, haystack):
    if distance == 0:
        intervener = r"(\W*)"
    else:
        intervener = r"((\W*)(\b['\w]*\b)(\W*)){0," +str(distance)+ r"}"

    finder1 = re.compile(r"(\b['\w]*)"+needle1+r"(['\w]*\b)"+intervener+r"(\b['\w]*)"+needle2+r"(['\w]*\b)", re.IGNORECASE)
    finder2 = re.compile(r"(\b['\w]*)"+needle2+r"(['\w]*\b)"+intervener+r"(\b['\w]*)"+needle1+r"(['\w]*\b)", re.IGNORECASE)
    matches1 = finder1.findall(haystack)
    matches2 = finder2.findall(haystack)
    iter1 = finder1.finditer(haystack)
    iter2 = finder2.finditer(haystack)
    sum1 = sum(1 for _ in finder1.finditer(haystack))
    sum2 = sum(1 for _ in finder2.finditer(haystack))
    return sum1 + sum2



def getwords(text):
    return re.findall(r"\b['\w]+\b", text)

def getwordpairs(text):    
    return re.findall(r"(\b['\w]+\b)(?=\W+(?=(\b['\w]+\b)))", text)

