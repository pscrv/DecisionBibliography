import django
from django.test import TestCase

# TODO: Configure your database in settings.py and sync before running tests.

class DBProxy2Tests(TestCase):

    if django.VERSION[:2] >= (1, 7):
        # Django 1.7 requires an explicit setup() when running tests in PTVS
        @classmethod
        def setUpClass(cls):
            super(DBProxy2Tests, cls).setUpClass()
            django.setup()


    def test_DecisionModelProxy_GetFilteredOnBibliographyKeywords(self):
        from Decisions.DBProxy2 import DecisionModelProxy
        casenumber = 'T 0641/00'
        result = DecisionModelProxy.GetFilteredOnBibliographyKeywords(CaseNumber = casenumber)
        self.assertEqual(len(result), 3)
        for r in result:
            self.assertEqual(r.CaseNumber, casenumber)

    def test_DecisionModelProxy_GetFilteredOnTextKeywords(self):
        from Decisions.DBProxy2 import DecisionModelProxy
        word = 'umfasst'
        result = DecisionModelProxy.GetFilteredOnTextKeywords(Reasons__contains = word)
        test = [x for x in result if x.CaseNumber == 'T 0336/15']
        self.assertNotEqual(test, [])




