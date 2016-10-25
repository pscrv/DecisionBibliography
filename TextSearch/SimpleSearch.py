
import operator
from functools import reduce
from django.db.models import Q


class SimpleTextSearcher(object):

    def __init__(self, terms: list):
        self.__terms = terms

        from app.DBProxy import DecisionModelProxy
        textResult = DecisionModelProxy.GetTextsFiltered()        
        for term in self.__terms:
            textResult = textResult.filter(
                (Q(Facts__contains = term) |
                 Q(Reasons__contains = term) |
                 Q(Order__contains = term)))
        self.__result = [result.decision for result in textResult]

    @property
    def Result(self):
        return self.__result