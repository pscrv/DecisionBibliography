
import operator
from functools import reduce
from django.db.models import Q

from Decisions.DBProxy import DecisionModelProxy


class SimpleTextSearcher(object):

    @property
    def Results(self):
        return self.__results

    def __init__(self, terms: list):
        self.__terms = terms
        self.__resultsDictionary = {}
        self.__haveAllTerms = {}
        self.__results = {}
        self.__locationCounts = {}
                
        if terms == None or terms == []:
            return

        for term in self.__terms:
            self.__searchOneTerm(term)
        self.__collectResults()
        if self.__haveAllTerms == {}:
            return

        self.__countLocations()
        self.__collateResults()



    def __searchOneTerm(self, term):
        self.__resultsDictionary[term] = SearchResult(
            term = term,
            inCatchwords = self.__makeSetFromBibl('Catchwords', term),
            inKeywords = self.__makeSetFromBibl('Keywords', term),
            inFacts = self.__makeSetFromText('Facts', term),
            inReaons = self.__makeSetFromText('Reasons', term),
            inOrder = self.__makeSetFromText('Order', term),
            )


    def __makeSetFromBibl(self, kw, term):
        return {x.pk for x in DecisionModelProxy.GetBibliographyFiltered(**{kw + '__contains': term })}

    
    def __makeSetFromText(self, kw, term):
        return {x.decision.pk for x in DecisionModelProxy.GetTextsFiltered(**{kw + '__contains': term })}



    def __collectResults(self):
        self.__haveAllTerms = set.intersection(*[self.__resultsDictionary[x].InAny for x in self.__resultsDictionary])


    def __countLocations(self):
        for term in self.__resultsDictionary:
            searchResult = self.__resultsDictionary[term]
            self.__locationCounts[term] = {}
            self.__locationCounts[term]['CatchwordCount'] = 0
            self.__locationCounts[term]['KeywordCount'] = 0
            self.__locationCounts[term]['FactsCount'] = 0
            self.__locationCounts[term]['ReasonsCount'] = 0
            self.__locationCounts[term]['OrderCount'] = 0

            for result in self.__haveAllTerms:
                if result in searchResult.InCatchwords:
                    self.__locationCounts[term]['CatchwordCount'] += 1
                if result in searchResult.InKeywords:
                    self.__locationCounts[term]['KeywordCount'] += 1
                if result in searchResult.InFacts:
                    self.__locationCounts[term]['FactsCount'] += 1
                if result in searchResult.InReasons:
                    self.__locationCounts[term]['ReasonsCount'] += 1
                if result in searchResult.InOrder:
                    self.__locationCounts[term]['OrderCount'] += 1


    def __collateResults(self):
        for result in self.__haveAllTerms:
            self.__results[result] = {}
            self.__results[result]['Catchwords'] = 0
            self.__results[result]['Keywords'] = 0
            self.__results[result]['Facts'] = 0
            self.__results[result]['Reasons'] = 0
            self.__results[result]['Order'] = 0
            for term in self.__terms:
                searchResult = self.__resultsDictionary[term]
                if result in searchResult.InCatchwords:
                    self.__results[result]['Catchwords'] += 1
                if result in searchResult.InKeywords:
                    self.__results[result]['Keywords'] += 1
                if result in searchResult.InFacts:
                    self.__results[result]['Facts'] += 1
                if result in searchResult.InReasons:
                    self.__results[result]['Reasons'] += 1
                if result in searchResult.InOrder:
                    self.__results[result]['Order'] += 1







class SearchResult(object):
    
    def __init__(self, term, inCatchwords, inKeywords, inFacts, inReaons, inOrder):
        self.Terms = [term]
        self.InCatchwords = inCatchwords
        self.InKeywords = inKeywords
        self.InFacts = inFacts
        self.InReasons = inReaons
        self.InOrder = inOrder
        self.__set__InAny()

    def __set__InAny(self):
        allLists = [self.InCatchwords, self.InKeywords, self.InFacts, self.InReasons, self.InOrder]
        self.InAny = {x for pklist in allLists for x in pklist}

