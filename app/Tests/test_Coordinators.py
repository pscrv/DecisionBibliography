
import django
from django.test import TestCase


class test_PersistentAnalysisCoordinator(TestCase):
        
    @classmethod
    def setUpClass(cls):    
        super(test_PersistentAnalysisCoordinator, cls).setUpClass()
        django.setup()
        
    def setUp(self):
        from Analysers.Coordinators import PersistentAnalysisCoordinator
        self.coordinator = PersistentAnalysisCoordinator()
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
