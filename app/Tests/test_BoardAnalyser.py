from datetime import datetime, timedelta
import django
from django.test import TestCase

from Analysers.BoardAnalysis import *


class test_BoardAnalyser(TestCase):
        
    @classmethod
    def setUpClass(cls):    
        super(test_BoardAnalyser, cls).setUpClass()
        django.setup()
        
    def setUp(self):
        from Analysers.BoardAnalyser import BoardAnalyser
        self.analyser = BoardAnalyser()

    def test_GetAnalysisReturnsSomething(self):
        x = self.analyser.GetAnalysis('3.5.01')
        self.assertFalse(x == None)

    def test_GetAnalysisIsNotOutofdate(self):
        x = self.analyser.GetAnalysis('3.5.01')
        y = self.analyser.GetAnalysis('NoneExistantBoard')
        outdated = OutdatedBoardAnalysis()
        self.assertFalse(x == outdated)
        self.assertFalse(y == outdated)

    def test_GetAnalysisOnlyNullForNoneBoard(self):
        realBoard = '3.5.01'
        unrealBoard = 'nonesense'
        real = self.analyser.GetAnalysis(realBoard)
        unreal = self.analyser.GetAnalysis(unrealBoard)
        self.assertEqual(unreal, NullBoardAnalysis(), 'unreal board did not return NullBoardAnalysis')
        self.assertNotEqual(real, NullBoardAnalysis(), 'real board returned NullBoardAnalysis')

    def test_GetAnalysis3501(self):
        board = '3.5.01'
        analysis = self.analyser.GetAnalysis(board)
        self.assertEqual(analysis.Board, board)
        self.assertEqual(analysis.Count, 321)
        self.assertEqual(len(analysis.IpcTop5), 5)
        self.assertEqual(len(analysis.ArticleTop5), 5)
        self.assertEqual(len(analysis.CitationTop5), 5)

    def test_removeOldFromCache(self):
        board1 = '3.5.01'
        board2 = '3.1.01'
        a1 = self.analyser.GetAnalysis(board1)
        a2 = self.analyser.GetAnalysis(board2)
        cachedBoards1 = self.analyser.CachedBoardList
        a1.Timestamp = datetime.now() - timedelta(days = 2)
        a2.Timestamp = datetime.now()
        a3 = self.analyser.GetAnalysis(board2)
        cachedBoards2 = self.analyser.CachedBoardList
        self.assertTrue(board1 in cachedBoards1 and board2 in cachedBoards1)
        self.assertFalse(board1 in cachedBoards2)
        self.assertTrue(board2 in cachedBoards2)
        



