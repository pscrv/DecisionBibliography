


class Issue(object):

    def __init__(self, name: str):
        self.__name = name
        self.__textSearchTerms = []

    @property
    def Name(self):
        return self.__name

    @property
    def CanAnalyse(self):
        return True


    def SetTextsearchTerms(self, termList):
        self.__textSearchTerms = termList

    def GetTextSearchTerms(self):
        return self.__textSearchTerms



class NullIssue(Issue):
    
    def __init__(self, name: str = ''):
        super(NullIssue, self).__init__('nullIssue')


    def __eq__(self, other):
        if isinstance(other, NullIssue):
            return True
        return False


    @property
    def CanAnalyse(self):
        return False