from datetime import datetime, timedelta
import django
from django.test import TestCase


class test_BoardTimelineAnalyser(TestCase):
        
    @classmethod
    def setUpClass(cls):    
        super(test_BoardTimelineAnalyser, cls).setUpClass()
        django.setup()
        
    def setUp(self):
        from Analysers.TimelineAnalysers import BoardTimelineAnalyser, NullBoardTimelineAnalysis
        from Analysers.AnalysisBase import OutdatedAnalysis
        self.analyser = BoardTimelineAnalyser()
        self.outdated = OutdatedAnalysis()
        self.nullanalysis = NullBoardTimelineAnalysis()
        self.realBoard = '3.5.01'
        self.falseBoard = 'NoneExistantBoard'

    def test_GetAnalysisReturnsSomething(self):
        x = self.analyser.GetAnalysis(self.realBoard)
        self.assertFalse(x == None)

    def test_AnalysisIsNotOutofdate(self):
        x = self.analyser.GetAnalysis(self.realBoard)
        y = self.analyser.GetAnalysis(self.falseBoard)
        self.assertFalse(x == self.outdated)
        self.assertFalse(y == self.outdated)
        
    def test_AnalysisOnlyNullForNonBoard(self):
        real = self.analyser.GetAnalysis(self.realBoard)
        unreal = self.analyser.GetAnalysis(self.falseBoard)
        self.assertEqual(unreal, self.nullanalysis, 'unreal board did not return NullBoardAnalysis')
        self.assertNotEqual(real, self.nullanalysis, 'real board returned NullBoardAnalysis')

    def test_YearlyDecisionsNotEmpty(self):
        real = self.analyser.GetAnalysis(self.realBoard)
        self.assertNotEqual (real.YearlyDecisions, None)

    def test_YearlyDecisionsCountFor3501_to1999(self):
        real = self.analyser.GetAnalysis(self.realBoard)
        countYears = [year for year in real.YearlyDecisions if year <= 1999]
        self.assertEqual(len(countYears), 18)
        
    def test_TotalDecisionsCountFor3501_to1999(self):
        real = self.analyser.GetAnalysis(self.realBoard)
        to1999 = [v for k,v in real.YearlyDecisions.items() if v <= 1999]
        self.assertEqual(sum(to1999), 321)

    def test_AnalysesAreCached(self):
        board1 = self.realBoard
        board2 = '3.1.01'
        a1 = self.analyser.GetAnalysis(board1)
        self.assertTrue(board1 in self.analyser.CachedBoardList, 'First analysis: board1')
        a2 = self.analyser.GetAnalysis(board2)
        self.assertTrue(board2 in self.analyser.CachedBoardList, 'Second analysis: board2')
        self.assertTrue(board1 in self.analyser.CachedBoardList, 'Second analysis: board2')
        a3 = self.analyser.GetAnalysis(board1)
        self.assertTrue(board2 in self.analyser.CachedBoardList, 'Third analysis: board1')
        self.assertTrue(board1 in self.analyser.CachedBoardList, 'Third analysis: board1')
        self.assertEqual(len(self.analyser.CachedBoardList), 2, 'Cache should contain two boards')

        
    def test_removeOldFromCache(self):
        board1 = self.realBoard
        board2 = '3.1.01'
        a1 = self.analyser.GetAnalysis(board1)
        a2 = self.analyser.GetAnalysis(board2)
        cachedBoards1 = self.analyser.CachedBoardList
        a1.Timestamp = datetime.now() - timedelta(days = 2)
        a2.Timestamp = datetime.now()
        a3 = self.analyser.GetAnalysis(board2)
        cachedBoards2 = self.analyser.CachedBoardList
        self.assertTrue(board1 in cachedBoards1)
        self.assertTrue(board2 in cachedBoards1)
        self.assertFalse(board1 in cachedBoards2)
        self.assertTrue(board2 in cachedBoards2)







