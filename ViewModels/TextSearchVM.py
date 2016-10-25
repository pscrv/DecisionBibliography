from ViewModels.Base import VMBase
from TextSearch.SimpleSearch import SimpleTextSearcher

class TextSearchViewModel(VMBase):

    def __init__(self, query):
        super(TextSearchViewModel, self).__init__()
        self.__query = query.lower()

        if self.__query == '':
            self.__setMiniContext()
        else:
            self.__getSearchResults()
            self.__extractResults()
            self.__setFullcontext()
        

    
    def __getSearchResults(self):
        searchTerms = [x for x in self.__query.split(',')]
        searcher = SimpleTextSearcher(searchTerms)
        self.__results = searcher.Result


    def __extractResults(self):
        self.__extractedResults = [
            TextSearchResult(
                result, 
                self.__getTextExtracts(result)) for result in self.__results]


    def __getTextExtracts(self, decision):
        from app.DBProxy import DecisionModelProxy
        import re
        terms = '|'.join(self.__query.split(','))
        finder = re.compile(r'((?:\w+\W+){,7})(' + terms + ')\W+((?:\w+\W+){,7})', re.IGNORECASE)

        text = DecisionModelProxy.GetTextFromDecision(decision)
        fullText = '\n\n'.join([text.Facts, text.Reasons, text.Order])
        
        found = re.search(finder, fullText)
        if found:
            extract = '... ' + ' '.join([ x.strip() for x in found.groups()]) + ' ...'
        else:
            extract = ''
        return extract




    def __setMiniContext(self):
        self.Context.update( {
            'title': 'Text Search',
            'message': '',  
            'result': [],
            } )

    def __setFullcontext(self):
        self.Context.update( {
            'title': 'Text Search',
            'message': self.__query + ': ' + str(len(self.__results)) + ' results',
            'results': self.__extractedResults,
            } )


class TextSearchResult(object):

    def __init__(self, decision, text):
        self.Decision = decision
        self.TextExtract = text

