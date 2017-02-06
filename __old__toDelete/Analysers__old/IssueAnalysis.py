
from Analysers.AnalysisBase import TimestampBase

class IssueAnalysis(TimestampBase):
    
    def __init__(self, issue, results): 
        super(IssueAnalysis, self).__init__()
        self.__issue = issue
        self.__results = results

    @property
    def Issue(self):
        return self.__issue

    @property
    def Results(self):
        return self.__results



class NullIssueAnalysis(IssueAnalysis):

    def __init__(self):
        super(NullIssueAnalysis, self).__init__('Nosuchissue', None)

                
    def __eq__(self, other):
        if isinstance(other, NullIssueAnalysis):
            return True
        return False

    @property
    def IsValid(self):
        return False