
import django
from django.test import TestCase

from Issues.Issue import Issue

class test_Issues(TestCase):
        
    @classmethod
    def setUpClass(cls):    
        super(test_Issues, cls).setUpClass()
        django.setup()
        
    def setUp(self):
        self.arbitraryName = 'Any string'
        self.testIssueName = 'testIssue'

    def test_initialiseName(self):
        issue = Issue(self.arbitraryName)
        self.assertEqual(issue.Name, self.arbitraryName)
    
    def test_TestIssueHasTextSearchTerms(self):
        issue = Issue(self.testIssueName)
        self.assertTrue(issue.GetTextSearchTerms() is not None)

    def test_TestSetTextSearchTerms(self):  
        terms = ['medicinal', 'use']      
        issue = Issue(self.testIssueName)
        issue.SetTextsearchTerms(terms)
        issueTerms = issue.GetTextSearchTerms()
        self.assertEqual(len(issueTerms), 2)
        self.assertTrue('medicinal' in issueTerms)
        self.assertTrue('use' in issueTerms)
