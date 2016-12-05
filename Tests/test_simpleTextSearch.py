import django
from django.test import TestCase

class test_SimpleTextSearcher(TestCase):
        
    @classmethod
    def setUpClass(cls):    
        super(test_SimpleTextSearcher, cls).setUpClass()
        django.setup()
        
    def setUp(self):
        from TextSearch.SimpleSearch import SimpleTextSearcher
        self.searcher = SimpleTextSearcher(['legal', 'board'])

    def test_findsG1_97(self):
        result = self.searcher.Results
        resultList = [a.decision.CaseNumber for a in result]
        self.assertTrue('G 0001/97' in resultList)