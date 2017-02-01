import re

from Decisions.DBProxy import DecisionModelProxy
from Decisions.ViewModels.Base import VMBase
from Decisions.TextSearch.SimpleSearch import SimpleTextSearcher

class TextSearchViewModel(VMBase):

    def __init__(self, query):
        super(TextSearchViewModel, self).__init__()
        self.__query = [x.strip() for x in query.lower().split(',')]   
        self.__sorts = ['Catchwords', 'Keywords', 'Reasons', 'Facts', 'Order']

        if self.__query == ['']:
            self.__setMiniContext()
        else:
            self.__getSearchResults()
            self.__extractResults()
            self.__setFullcontext()
        


    def __setMiniContext(self):
        self.Context.update( {
            'title': 'Text Search',
            'message': '',  
            'results': [],
            'highlightterms': []
            } )

    def __setFullcontext(self):
        self.Context.update( {
            'title': 'Text Search',
            'message': ','.join(self.__query) + ': ' + str(len(self.__results)) + ' results',
            'results': self.__extractedResults,
            'highlightterms': self.__query
            } )


    
    def __getSearchResults(self):
        searcher = SimpleTextSearcher(self.__query)
        self.__results = searcher.Results
        self.__collatedResults = {x: [] for x in self.__sorts}
        for result in self.__results:
            for sort in self.__sorts:
                if self.__results[result][sort] > 0:
                    self.__collatedResults[sort].append(result)
                    break

                
    def __extractResults(self):
        self.__extractedResults = []
        for sort in self.__sorts:
            for result in self.__collatedResults[sort]:
                decision = DecisionModelProxy.GetDecisionFromPrimaryKey(result)
                extract = self.__getTextExtract(decision, sort)
                self.__extractedResults.append(
                    TextSearchResult(
                        decision,
                        extract,
                        )
                    )



    def __getTextExtract(self, decision, sort):
        searchText = decision.__dict__.get(sort, '')

        terms = '|'.join([x.strip() for x in (self.__query)] )
        finder = re.compile(r'(\S+\s+){0,11}(' + terms + r'(?:\S*))(\s+\S+){0,11}', re.IGNORECASE)
        found = re.search(finder, searchText)

        if found:
            result = '[' + sort + '] ... ' + found.group() + ' ...'
        else:
            result = '[' + sort + '] ... something went wrong ...'
        return result




class TextSearchResult(object):

    def __init__(self, decision, extract):
        self.Decision = decision
        self.TextExtract = extract

