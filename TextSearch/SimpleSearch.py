
import operator
from functools import reduce
from django.db.models import Q


class SimpleTextSearcher(object):

    def __init__(self, terms: list):
        self.__terms = terms

        from app.DBProxy import DecisionModelProxy
        self.__result = DecisionModelProxy.GetTextsFiltered()        
        for term in self.__terms:
            self.__result = self.__result.filter(
                (Q(Facts__contains = term) |
                 Q(Reasons__contains = term) |
                 Q(Order__contains = term)))

    @property
    def Result(self):
        return self.__result