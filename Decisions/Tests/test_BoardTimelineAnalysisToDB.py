import django
from django.test import TestCase



class test_BoardTimelinedAnalysisToDB(TestCase):
        
    @classmethod
    def setUpClass(cls):    
        super(test_BoardTimelinedAnalysisToDB, cls).setUpClass()
        django.setup()
        
    def setUp(self):
        from Decisions.Analysers.TimelineAnalysis import BoardTimelineAnalysis
        self.realBoard = '3.5.01'
        self.falseBoard = 'not a real board'


    def test_GetRealBoard(self):
        from Decisions.AnalysisStorers import BoardTimelineAnalysisToDB
        retreived = BoardTimelineAnalysisToDB.GetBoardTimelineAnalysisFromDB(self.realBoard)
        to1999 = [v for k, v in retreived.YearlyDecisions.items() if k <= 1999]        
        countYears = [year for year in retreived.YearlyDecisions if year <= 1999]
        self.assertEqual(retreived.Board, self.realBoard)
        self.assertEqual(sum(to1999), 863)
        self.assertEqual(len(countYears), 18)


    def test_GetUnrealBoard(self):
        from Decisions.AnalysisStorers import BoardTimelineAnalysisToDB
        from Decisions.Analysers.TimelineAnalysis import NullBoardTimelineAnalysis
        retreived = BoardTimelineAnalysisToDB.GetBoardTimelineAnalysisFromDB(self.falseBoard)
        to1999 = [v for k, v in retreived.YearlyDecisions.items() if v <= 1999]        
        countYears = [year for year in retreived.YearlyDecisions if year <= 1999]
        self.assertEqual(retreived.Board, 'Nosuchboard')
        self.assertEqual(sum(to1999), 0)
        self.assertEqual(len(countYears), 0)
        self.assertIsInstance(retreived, NullBoardTimelineAnalysis)


        
    def test_SaveAndRetreive(self):
        from Decisions.AnalysisStorers import BoardTimelineAnalysisToDB
        from Decisions.Analysers.TimelineAnalysers import BoardTimelineAnalyser

        board = '3.5.01'
        analyser = BoardTimelineAnalyser()
        before = analyser.GetAnalysis(board)
        before.Board = 'test'
        BoardTimelineAnalysisToDB.SaveBoardTimelineAnalysisToDB(before)
        after = BoardTimelineAnalysisToDB.GetBoardTimelineAnalysisFromDB('test')
        self.assertEqual(after.Board, before.Board)





