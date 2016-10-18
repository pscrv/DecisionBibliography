
import unittest
from datetime import datetime


from Analysers.BoardAnalysis import *

class test_BoardAnalysis(unittest.TestCase):
            
    def test_OutdatedBoardAnalysis(self):
        analysis = OutdatedBoardAnalysis()
        self.assertEqual(analysis.Board, 'Outofdate')
        self.assertEqual(analysis.Timestamp, datetime.min)        

    def test_OutdatedBoardAnalysisEquality(self):
        x = OutdatedBoardAnalysis()
        y = OutdatedBoardAnalysis()
        self.assertEqual(x, y)

                
    def test_NullBoardAnalysis(self):
        analysis = NullBoardAnalysis()
        self.assertEqual(analysis.Board, 'Nosuchboard')       

    def test_NullBoardAnalysisEquality(self):
        x = NullBoardAnalysis()
        y = NullBoardAnalysis()
        self.assertEqual(x, y)


    def test_Age(self):
        newAnalysis = BoardAnalysis()
        oldAnalysis = OutdatedBoardAnalysis()
        newAge = newAnalysis.Age
        oldAge = oldAnalysis.Age
        self.assertTrue(newAge.days < 1)
        self.assertTrue(oldAge.days > 700000)

        

if __name__ == '__main__':
    unittest.main()