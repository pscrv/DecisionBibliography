from datetime import datetime, timedelta
import django
from django.test import TestCase

from Decisions.Analysers.BoardAnalysis import *


def setUpModule():
    from Decisions.Analysers.BoardAnalyser import BoardAnalyser
    from Decisions.Analysers.AnalysisBase import OutdatedAnalysis
    analyser = BoardAnalyser()
    outdatedAnalysis = OutdatedAnalysis()
    legalBoard = '3.1.01'
    realBoard = '3.5.07'
    falseBoard = 'NoneExistantboard'
    legalBoardAnalysis = self.analyser.GetAnalysis(self.legalBoard)
    realBoardAnalysis = self.analyser.GetAnalysis(self.realBoard)
    falseBoardAnalysis = self.analyser.GetAnalysis(self.falseBoard)


class test_BoardAnalyser(TestCase):
        
    @classmethod
    def setUpClass(cls):    
        super(test_BoardAnalyser, cls).setUpClass()
        django.setup()
        


    def setUp(self):
        from Decisions.Analysers.BoardAnalyser import BoardAnalyser
        from Decisions.Analysers.AnalysisBase import OutdatedAnalysis
        self.analyser = BoardAnalyser()
        self.outdatedAnalysis = OutdatedAnalysis()
        self.legalBoard = '3.1.01'
        self.realBoard = '3.5.07'
        self.falseBoard = 'NoneExistantboard'
        self.legalBoardAnalysis = self.analyser.GetAnalysis(self.legalBoard)
        self.realBoardAnalysis = self.analyser.GetAnalysis(self.realBoard)
        self.falseBoardAnalysis = self.analyser.GetAnalysis(self.falseBoard)

    def test_GetAnalysisReturnsSomething(self):
        self.assertFalse(self.realBoardAnalysis is None)

    def test_GetAnalysisIsNotOutofdate(self):
        self.assertFalse(self.realBoardAnalysis == self.outdatedAnalysis)
        self.assertFalse(self.falseBoardAnalysis == self.outdatedAnalysis)

    def test_GetAnalysisOnlyNullForNoneBoard(self):
        self.assertEqual(self.falseBoardAnalysis, NullBoardAnalysis(), 'unreal board did not return NullBoardAnalysis')
        self.assertNotEqual(self.realBoardAnalysis, NullBoardAnalysis(), 'real board returned NullBoardAnalysis')

    def test_GetAnalysisOfBoard(self):
        self.assertEqual(self.realBoardAnalysis.Board, self.realBoard)
        self.assertTrue(self.realBoardAnalysis.Count > 100)
        self.assertEqual(len(self.realBoardAnalysis.IpcTop5), 5)
        self.assertEqual(len(self.realBoardAnalysis.ArticleTop5), 5)
        self.assertEqual(len(self.realBoardAnalysis.CitationTop5), 5)

    def test_removeOldFromCache(self):
        board1 = self.realBoard
        board2 = self.legalBoard
        a1 = self.realBoardAnalysis
        a2 = self.legalBoardAnalysis
        cachedBoards1 = self.analyser.CachedBoardList
        a1.Timestamp = datetime.now() - timedelta(days = 2)
        a2.Timestamp = datetime.now()
        a3 = self.analyser.GetAnalysis(board2)
        cachedBoards2 = self.analyser.CachedBoardList
        self.assertTrue(board1 in cachedBoards1 and board2 in cachedBoards1)
        self.assertFalse(board1 in cachedBoards2)
        self.assertTrue(board2 in cachedBoards2)
        



