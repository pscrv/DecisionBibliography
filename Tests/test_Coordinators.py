
import django
from django.test import TestCase


class test_PersistentBoardAnalysisCoordinator(TestCase):
        
    @classmethod
    def setUpClass(cls):    
        super(test_PersistentBoardAnalysisCoordinator, cls).setUpClass()
        django.setup()
        
    def setUp(self):
        from Analysers.Coordinators import PersistentBoardAnalysisCoordinator
        self.coordinator = PersistentBoardAnalysisCoordinator()
        self.realBoard = '3.5.01'
        self.falseBoard = 'notarealboard'

    def test_GetAnalysisReturnsSomething(self):
        x = self.coordinator.GetAnalysis(self.realBoard)
        self.assertFalse(x is None)

    def test_CanRetreiveRealBoard(self):
        x = self.coordinator.GetAnalysis(self.realBoard)
        self.assertTrue(x.Board == self.realBoard)
        self.assertTrue(x.IsValid)

    def test_CannotRetreiveFalseBoard(self):
        x = self.coordinator.GetAnalysis(self.falseBoard)
        self.assertFalse(x.IsValid)

    
class test_PersistentTimelineAnalysisCoordinator(TestCase):
        
    @classmethod
    def setUpClass(cls):    
        super(test_PersistentTimelineAnalysisCoordinator, cls).setUpClass()
        django.setup()
        
    def setUp(self):
        from Analysers.Coordinators import PersistentTimelineAnalysisCoordinator
        self.coordinator = PersistentTimelineAnalysisCoordinator()
        self.realBoard = '3.5.01'
        self.falseBoard = 'notarealboard'

    def test_GetAnalysisReturnsSomething(self):
        x = self.coordinator.GetAnalysis(self.realBoard)
        self.assertFalse(x is None)

    def test_CanRetreiveRealBoard(self):
        x = self.coordinator.GetAnalysis(self.realBoard)
        self.assertTrue(x.Board == self.realBoard)

    def test_CannotRetreiveFalseBoard(self):
        x = self.coordinator.GetAnalysis(self.falseBoard)
        self.assertFalse(x.IsValid)

