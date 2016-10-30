import re

from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(needs_autoescape=True)
def highlight(text, words, autoescape=True): 

    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x

    for word in words:
        finder = re.compile(word, re.IGNORECASE)
        found = finder.search(text)
        if found:
            wordToHighlight = found.group()
        else:
            continue
        
        substitute = '<span class=''highlight''>' + esc(wordToHighlight) + '</span>'
        text = finder.sub(substitute, text)

    return mark_safe(text)
       

    

    #finder = re.compile('|'.join(words), re.IGNORECASE)

    #found = finder.search(text)
    #if found:
    #    wordToHighlight = found.group()
    #else:
    #    return text
    #result = mark_safe(substitutedText)
    #return result



