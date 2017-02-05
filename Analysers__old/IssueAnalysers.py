from datetime import timedelta

from app.DBProxy import DecisionModelProxy

from Analysers.AnalyserBase import CachingBase
from Analysers.IssueAnalysis import IssueAnalysis, NullIssueAnalysis
from Issues.Issue import Issue, NullIssue
from Issues.IssuesProvider import IssuesCollection

class IssueAnalyser(CachingBase):
    
    def __init__(self, cachetimelimit: timedelta = timedelta(days=1)):
        super(IssueAnalyser, self).__init__(cachetimelimit)
        self.__issuesProvider = IssuesCollection()


    def IsCached(self, issueName):        
        return issueName in self._cachedKeyList()
        

    def _analyseAndCache(self, issueName):

        foundIssue = self.__issuesProvider.GetIssueFromName(issueName)
        analysis = self.__analyse(foundIssue)        
        self._cache[issueName] = analysis
        return analysis

    def __analyse(self, issue: Issue):
        if issue.CanAnalyse:
            textSearchTerms = issue.GetTextSearchTerms()
            results = DecisionModelProxy.GetDecisionListFromTextSearchANDTermList(textSearchTerms)
            return IssueAnalysis(issue, results)
        else:
            return NullIssueAnalysis()








