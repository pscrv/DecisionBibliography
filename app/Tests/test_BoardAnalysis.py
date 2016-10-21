
import unittest
from datetime import datetime


from Analysers.AnalysisBase import OutdatedAnalysis
from Analysers.BoardAnalysis import *

class test_BoardAnalysis(unittest.TestCase):
            
    def test_OutdatedAnalysis(self):
        analysis = OutdatedAnalysis()
        self.assertEqual(analysis.Timestamp, datetime.min)        

    def test_OutdatedBoardAnalysisEquality(self):
        x = OutdatedAnalysis()
        y = OutdatedAnalysis()
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
        oldAnalysis = OutdatedAnalysis()
        newAge = newAnalysis.Age
        oldAge = oldAnalysis.Age
        self.assertTrue(newAge.days < 1)
        self.assertTrue(oldAge.days > 700000)

        

if __name__ == '__main__':
    unittest.main()
