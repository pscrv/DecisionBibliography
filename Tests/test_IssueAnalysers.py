
import django
from django.test import TestCase

#from Analysers.IssueAnalysers import IssueAnalyser
from Analysers.IssueAnalysis import IssueAnalysis, NullIssueAnalysis
from Issues.Issue import Issue, NullIssue

class test_IssueAnalyser(TestCase):
        
    @classmethod
    def setUpClass(cls):    
        super(test_IssueAnalyser, cls).setUpClass()
        django.setup()
        
    def setUp(self):
        from Analysers.IssueAnalysers import IssueAnalyser
        self.analyser = IssueAnalyser()
        self.nullIssueAnalysis = NullIssueAnalysis()
        self.falseIssue = NullIssue()
        self.testIssueName = 'testIssue'
        self.arbitraryIssueName = 'anyIssue'
        self.nonIssueName = 'nonIssue'

    def test_GetAnalysisReturnsSomething(self):
        x = self.analyser.GetAnalysis(self.arbitraryIssueName)
        self.assertFalse(x is None)

    def test_IssueIsValid(self):
        x = self.analyser.GetAnalysis(self.testIssueName)
        self.assertTrue(x.IsValid)

    def test_NonIssueIsNotValid(self):
        x = self.analyser.GetAnalysis(self.nonIssueName)
        self.assertFalse(x.IsValid)

    def test_issueIsCached(self):
        isCachedAtStart = self.analyser.IsCached(self.testIssueName)
        x = self.analyser.GetAnalysis(self.testIssueName)
        isCachedAtEnd = self.analyser.IsCached(self.testIssueName)
        self.assertFalse(isCachedAtStart)
        self.assertTrue(isCachedAtEnd)

    def test_issueSearch(self):
        x = self.analyser.GetAnalysis(self.testIssueName)
        resultList = [a.decision.CaseNumber for a in x.Results]
        self.assertTrue('G 0001/97' in resultList)



