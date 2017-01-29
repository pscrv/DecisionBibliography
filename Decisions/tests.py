import django
from django.test import TestCase

# TODO: Configure your database in settings.py and sync before running tests.

class DecisionProxyTests(TestCase):

    if django.VERSION[:2] >= (1, 7):
        # Django 1.7 requires an explicit setup() when running tests in PTVS
        @classmethod
        def setUpClass(cls):
            super(DecisionProxyTests, cls).setUpClass()
            django.setup()


    def test_BadCaseNumberYieldsNullDecisionProxy(self):
        from Decisions.Decision import DecisionProxy
        casenumber = 'somerubbish'
        decisionproxy = DecisionProxy(casenumber)
        self.assertEqual(decisionproxy.DecisionDate, None)
        self.assertEqual(decisionproxy.FactsHeader, "No text available.")
        self.assertEqual(decisionproxy.ReasonsHeader, "No text available.")
        self.assertEqual(decisionproxy.OrderHeader, "No text available.")


    def test_DBNotEmpty(self):
        from Decisions.models import DecisionBibliographyModel
        entries = DecisionBibliographyModel.objects.count()
        x = 1









    # does not belong here
    # is not a test
    # just a stupid, if convenient, trigger
    def test_DBPopulator(self):
        from Decisions.management.utilities import DBPopulator
        populator = DBPopulator.BibliographyGetter()
        populator.GetAllForBoard('3.1.01')
        x = 1



