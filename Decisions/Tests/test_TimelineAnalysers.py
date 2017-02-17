from datetime import datetime, timedelta
import django
from django.test import TestCase


class test_BoardTimelineAnalyser(TestCase):
        
    @classmethod
    def setUpClass(cls):    
        super(test_BoardTimelineAnalyser, cls).setUpClass()
        django.setup()
        
    def setUp(self):
        from Decisions.Analysers.TimelineAnalysers import BoardTimelineAnalyser, NullBoardTimelineAnalysis
        from Decisions.Analysers.AnalysisBase import OutdatedAnalysis
        self.analyser = BoardTimelineAnalyser()
        self.outdated = OutdatedAnalysis()
        self.nullanalysis = NullBoardTimelineAnalysis()
        self.techBoard = '3.5.01'
        self.legalBoard = '3.1.01'
        self.falseBoard = 'NoneExistantBoard'
        self.realBoardAnalysis = self.analyser.GetAnalysis(self.techBoard)
        self.falseBoardAnalysis = self.analyser.GetAnalysis(self.falseBoard)
        self.legalBoardAnalysis = self.analyser.GetAnalysis(self.legalBoard)

    def test_GetAnalysisReturnsSomething(self):
        self.assertFalse(self.realBoardAnalysis is None)

    def test_AnalysisIsNotOutofdate(self):
        self.assertFalse(self.realBoardAnalysis == self.outdated)
        self.assertFalse(self.falseBoardAnalysis == self.outdated)
        
    def test_AnalysisOnlyNullForNonBoard(self):
        self.assertEqual(self.falseBoardAnalysis, self.nullanalysis, 'unreal board did not return NullBoardAnalysis')
        self.assertNotEqual(self.realBoardAnalysis, self.nullanalysis, 'real board returned NullBoardAnalysis')

    def test_YearlyDecisionsNotEmpty(self):
        self.assertNotEqual (self.realBoardAnalysis.YearlyDecisions, None)

    def test_YearlyDecisionsCountFor3501_to1999(self):
        countYears = [year for year in self.realBoardAnalysis.YearlyDecisions if year <= 1999]
        self.assertEqual(len(countYears), 18)
        
    def test_TotalDecisionsCountFor3501_to1999(self):
        to1999 = [v for k, v in self.realBoardAnalysis.YearlyDecisions.items() if v <= 1999]
        self.assertTrue(sum(to1999) > 1600)

    def test_AnalysesAreCached(self):
        board1 = self.techBoard
        board2 = self.legalBoard
        a1 = self.realBoardAnalysis
        self.assertTrue(board1 in self.analyser.CachedBoardList, 'First analysis: board1')
        a2 = self.legalBoardAnalysis
        self.assertTrue(board2 in self.analyser.CachedBoardList, 'Second analysis: board2')
        self.assertTrue(board1 in self.analyser.CachedBoardList, 'Second analysis: board1')
        a3 = self.analyser.GetAnalysis(board1) # do not replace by self.realBoardAnalysis
        self.assertTrue(board2 in self.analyser.CachedBoardList, 'Third analysis: board2')
        self.assertTrue(board1 in self.analyser.CachedBoardList, 'Third analysis: board1')

        
    def test_removeOldFromCache(self):
        board1 = self.techBoard
        board2 = self.legalBoard
        a1 = self.realBoardAnalysis
        a2 = self.legalBoardAnalysis
        cachedBoards1 = self.analyser.CachedBoardList
        a1.Timestamp = datetime.now() - timedelta(days = 2)
        a2.Timestamp = datetime.now()
        a3 = self.analyser.GetAnalysis(board2)
        cachedBoards2 = self.analyser.CachedBoardList
        self.assertTrue(board1 in cachedBoards1)
        self.assertTrue(board2 in cachedBoards1)
        self.assertFalse(board1 in cachedBoards2)
        self.assertTrue(board2 in cachedBoards2)







