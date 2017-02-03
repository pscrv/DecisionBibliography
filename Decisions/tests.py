import django
from django.test import TestCase

# TODO: Configure your database in settings.py and sync before running tests.

class DBProxyTests(TestCase):

    if django.VERSION[:2] >= (1, 7):
        # Django 1.7 requires an explicit setup() when running tests in PTVS
        @classmethod
        def setUpClass(cls):
            super(DBProxyTests, cls).setUpClass()
            django.setup()


    def test_DecisionModelProxy_GetFilteredOnBibliographyKeywords(self):
        from Decisions.DBProxy import DecisionModelProxy
        casenumber = 'T 0641/00'
        result = DecisionModelProxy.GetFilteredOnBibliographyKeywords(CaseNumber = casenumber)
        self.assertEqual(len(result), 3)
        for r in result:
            self.assertEqual(r.CaseNumber, casenumber)

    def test_DecisionModelProxy_GetFilteredOnTextKeywords(self):
        from Decisions.DBProxy import DecisionModelProxy
        word = 'umfasst'
        result = DecisionModelProxy.GetFilteredOnTextKeywords(Reasons__contains = word)
        test = [x for x in result if x.CaseNumber == 'T 0336/15']
        self.assertNotEqual(test, [])


    def test_DecisinModelProxy_GetAllForBoardOrderedByDecisionDate(self):
        from Decisions.DBProxy import DecisionModelProxy
        from Decisions.Analysers.BoardAnalyser import BoardAnalyser
        from Decisions.Analysers.TimelineAnalysers import BoardTimelineAnalyser

        board = '3.5.07'

        analyser = BoardAnalyser()
        result = analyser.GetAnalysis(board)
        self.assertEqual(result.Board, board)
        self.assertEqual(len(result.CitationTop5), 5)
        self.assertEqual(len(result.ArticleTop5), 5)
        self.assertEqual(len(result.IpcTop5), 5)
        self.assertEqual(len(result.Early), 5)
        self.assertEqual(len(result.Late), 5)
        self.assertTrue(result.Early[0].DecisionDate <= result.Late[0].DecisionDate)

        analyser = BoardTimelineAnalyser()
        result = analyser.GetAnalysis(board)
        self.assertEqual(result.Board, board)
        self.assertEqual(result.YearlyDecisions[2014], 38)

