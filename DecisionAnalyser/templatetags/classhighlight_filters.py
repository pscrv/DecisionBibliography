import re

from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(needs_autoescape=True)
def testfilter(text, autoescape=True): 
       
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x

    return mark_safe("TEST")
       

@register.filter(needs_autoescape=True)
def highlightclass(text, autoescape=True): 

    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x   

    #text, probability = text_tuple
    if probability > 0.5:
        text = '<a class="highlight">' + text + '</a>'

    return mark_safe(text)
       


@register.filter(needs_autoescape=True)
def highlight_and_link_casenumbers(text, autoescape=True): 

    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x
   
    finder = re.compile(r'([DGJRTW]\s*\d+/\d+)', re.IGNORECASE)
    text = finder.sub(r'<a class="highlight" href="/decisionFromCaseNumber/\1"> \1 </a>', text)

    return mark_safe(text)
       
