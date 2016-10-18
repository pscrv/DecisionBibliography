
import django
from django.test import TestCase

from Analysers.BoardAnalysis import *


class test_BoardAnalysisToDB(TestCase):
        
    @classmethod
    def setUpClass(cls):    
        super(test_BoardAnalysisToDB, cls).setUpClass()
        django.setup()
        

    def test_GetBoardAnalysisFromDB(self):
        from ObjectToDBConverters import BoardAnalysisToDB

        board = '3.5.01'
        x = BoardAnalysisToDB.GetBoardAnalysisFromDB(board)
        self.assertEqual(x.Board, board)
        self.assertEqual(x.Count, 321)


    def test_SaveAndRetreiveBoardAnalysisfromDB(self):
        from ObjectToDBConverters import BoardAnalysisToDB
        from Analysers.BoardAnalyser import BoardAnalyser

        board = '3.5.01'
        analyser = BoardAnalyser()
        before = analyser.GetAnalysis(board)
        before.Count = 1
        BoardAnalysisToDB.SaveBoardAnalysisToDB(before)
        after = BoardAnalysisToDB.GetBoardAnalysisFromDB(board)
        self.assertEqual(after.Board, before.Board)
        self.assertEqual(after.Count, before.Count)
        self.assertListEqual(after.Early, before.Early)
        self.assertListEqual(after.CitationTop5, before.CitationTop5)




