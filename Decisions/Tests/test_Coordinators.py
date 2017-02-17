
import django
from django.test import TestCase


class test_PersistentBoardAnalysisCoordinator(TestCase):
        
    @classmethod
    def setUpClass(cls):    
        super(test_PersistentBoardAnalysisCoordinator, cls).setUpClass()
        django.setup()
        
    def setUp(self):
        from Decisions.Analysers.Coordinators import PersistentBoardAnalysisCoordinator
        self.coordinator = PersistentBoardAnalysisCoordinator()
        self.realBoard = '3.5.01'
        self.falseBoard = 'notarealboard'

        self.realBoardAnalysis = self.coordinator.GetAnalysis(self.realBoard)


    def test_GetAnalysisReturnsSomething(self):
        self.assertFalse(self.realBoardAnalysis is None)

    def test_CanRetreiveRealBoard(self):
        self.assertTrue(self.realBoardAnalysis.Board == self.realBoard)
        self.assertTrue(self.realBoardAnalysis.IsValid)

    def test_CannotRetreiveFalseBoard(self):
        x = self.coordinator.GetAnalysis(self.falseBoard)
        self.assertFalse(x.IsValid)

    
class test_PersistentTimelineAnalysisCoordinator(TestCase):
        
    @classmethod
    def setUpClass(cls):    
        super(test_PersistentTimelineAnalysisCoordinator, cls).setUpClass()
        django.setup()
        
    def setUp(self):
        from Decisions.Analysers.Coordinators import PersistentTimelineAnalysisCoordinator
        self.coordinator = PersistentTimelineAnalysisCoordinator()
        self.realBoard = '3.5.01'
        self.falseBoard = 'notarealboard'
        self.realBoardAnalysis = self.coordinator.GetAnalysis(self.realBoard)

    def test_GetAnalysisReturnsSomething(self):
        self.assertFalse(self.realBoardAnalysis is None)

    def test_CanRetreiveRealBoard(self):
        self.assertTrue(self.realBoardAnalysis.Board == self.realBoard)

    def test_CannotRetreiveFalseBoard(self):
        x = self.coordinator.GetAnalysis(self.falseBoard)
        self.assertFalse(x.IsValid)

