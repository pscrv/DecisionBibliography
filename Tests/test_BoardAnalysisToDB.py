
import django
from django.test import TestCase

from Decisions.Analysers.BoardAnalysis import *


class test_BoardAnalysisToDB(TestCase):
        
    @classmethod
    def setUpClass(cls):    
        super(test_BoardAnalysisToDB, cls).setUpClass()
        django.setup()
        

    def test_GetBoardAnalysisFromDB(self):
        from Decisions.AnalysisStorers import BoardAnalysisToDB

        board = '3.5.01'
        x = BoardAnalysisToDB.GetBoardAnalysisFromDB(board)
        self.assertEqual(x.Board, board)
        self.assertTrue(x.Count > 1500)


    def test_SaveAndRetreiveBoardAnalysisfromDB(self):
        from Decisions.AnalysisStorers import BoardAnalysisToDB
        from Decisions.Analysers.BoardAnalyser import BoardAnalyser

        board = '3.5.07' #small board is faster
        analyser = BoardAnalyser()
        before = analyser.GetAnalysis(board)
        before.Count = 1
        beforeEarlyCaseNumbers = [x.CaseNumber for x in before.Early]
        beforeCitationsCaseNumber_Frequency = [(x.CaseNumber, y) for (x, y) in before.CitationTop5]
        BoardAnalysisToDB.SaveBoardAnalysisToDB(before)
        after = BoardAnalysisToDB.GetBoardAnalysisFromDB(board)
        afterEarlyCaseNumbers = [x.CaseNumber for x in after.Early]
        afterCitationsCaseNumber_Frequency = [(x.CaseNumber, y) for (x, y) in after.CitationTop5]
        self.assertEqual(after.Board, before.Board)
        self.assertEqual(after.Count, before.Count)
        self.assertListEqual(beforeEarlyCaseNumbers, afterEarlyCaseNumbers)
        self.assertListEqual(beforeCitationsCaseNumber_Frequency, afterCitationsCaseNumber_Frequency)




