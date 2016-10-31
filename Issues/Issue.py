


class Issue(object):

    def __init__(self, name: str):
        self.__name = name

    @property
    def Name(self):
        return self.__name

    @property
    def CanAnalyse(self):
        return True





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