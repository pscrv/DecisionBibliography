import django
from django.test import TestCase

class test_SimpleTextSearcher(TestCase):
        
    @classmethod
    def setUpClass(cls):    
        super(test_SimpleTextSearcher, cls).setUpClass()
        django.setup()
        
    def setUp(self):
        from Decisions.TextSearch.SimpleSearch import SimpleTextSearcher
        self.searcher = SimpleTextSearcher(['legal', 'board'])

    def test_findsG1_97(self):
        from Decisions.models import DecisionBibliographyModel
        correctpk = DecisionBibliographyModel.objects.FilterOnlyPrLanguage(CaseNumber = 'G 0001/97').first().pk
        result = self.searcher.Results
        self.assertTrue(correctpk in result)