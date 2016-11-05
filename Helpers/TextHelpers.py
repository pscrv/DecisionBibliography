import re

def countwords(text):
   return len(re.findall(r'\b\w+\b', text))

def countoccurences(needle, haystack):
    return sum(1 for _ in re.finditer(r'%s' % re.escape(needle), haystack))

def countwordoccurences(needle, haystack):
    return sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(needle), haystack))



