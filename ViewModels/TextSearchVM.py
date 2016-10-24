from ViewModels.Base import VMBase
from TextSearch.SimpleSearch import SimpleTextSearcher

class TextSearchViewModel(VMBase):
    
    def __init__(self, query):
        super(TextSearchViewModel, self).__init__()

        if query == '':
            results = None
        else:
            searchTerms = [x for x in query.split(',')]
            searcher = SimpleTextSearcher(searchTerms)
            results = searcher.Result

        self.Context.update( {
            'searchterms': query,
            'results': results,
            } )    


