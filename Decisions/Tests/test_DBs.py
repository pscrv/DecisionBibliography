import datetime
import django
from django.test import TestCase


class test_DecisionBibliographyModel(TestCase):
    
    @classmethod
    def setUpClass(cls):    
        super(test_DecisionBibliographyModel, cls).setUpClass()
        django.setup()
    
    
    def test_earliest(self):
        from Decisions.models import DecisionBibliographyModel as DB
        item = DB.objects.order_by('DecisionDate').first()
        self.assertEqual(item.CaseNumber, 'J 0002/78')
        self.assertEqual(item.DecisionDate, datetime.date(1979, 3, 1))
        
    def test_latestUpTo1999(self):
        from Decisions.models import DecisionBibliographyModel as DB
        datelimit = datetime.date(1999, 12, 31)
        item = DB.objects.FilterOnlyPrLanguage(DecisionDate__lte = datelimit).order_by('-DecisionDate').first()
        self.assertEqual(item.CaseNumber, 'T 0607/99')
        self.assertEqual(item.DecisionDate, datetime.date(1999, 12, 28))
        
    def test_3501Eearliest(self):
        from Decisions.models import DecisionBibliographyModel as DB
        item = DB.objects.FilterOnlyPrLanguage(Board = '3.5.01').order_by('DecisionDate').first()
        self.assertEqual(item.CaseNumber, 'T 0013/81')
        self.assertEqual(item.DecisionDate, datetime.date(1982, 1, 28))



class test_DecisionTextModel(TestCase):
     
    @classmethod
    def setUpClass(cls):    
        super(test_DecisionTextModel, cls).setUpClass()
        django.setup()    
    
    def test_earliest(self):
        from Decisions.models import DecisionTextModel as textDB, DecisionBibliographyModel as bibDB
        dec = bibDB.objects.FilterOnlyPrLanguage(CaseNumber = 'J 0002/78').first()
        item = textDB.objects.filter(Bibliography = dec).first()
        self.assertIsNotNone(item, 'Text of J 0002/78 is not in the database.')
        self.assertEqual(item.Reasons[0:33], 'Die Beschwerde richtet sich gegen')


class test_DecisionModelProxy(TestCase):

    @classmethod
    def setUpClass(cls):    
        super(test_DecisionModelProxy, cls).setUpClass()
        django.setup()

    def test_GetBoardList(self):
        from Decisions.DBProxy import DecisionModelProxy
        boards = DecisionModelProxy.GetBoardList()
        self.assertEqual(len(boards), 32)
        

        
class test_DBAnalyser(TestCase):

    @classmethod
    def setUpClass(cls):    
        super(test_DBAnalyser, cls).setUpClass()
        django.setup()
        
        
    def test_ipcFrequency(self):
        from Decisions.DBProxy import DecisionModelProxy
        from Decisions.Analysers import AnalysisHelpers
        decisions = DecisionModelProxy.GetListFromCaseNumber('G 0001/97')
        x = AnalysisHelpers.IpcFrequency(decisions)
        self.assertEqual(x['G04B 37/16'], 3)

    def test_ipcFrequencyForBoard(self):        
        from Decisions.Analysers import AnalysisHelpers
        x = AnalysisHelpers.IpcFrequencyForBoard('3.5.01')
        self.assertTrue(x['G06F 17/60'] > 150)

    def test_articleFrequency(self):
        from Decisions.DBProxy import DecisionModelProxy
        from Decisions.Analysers import AnalysisHelpers
        decisions = (DecisionModelProxy.GetListFromCaseNumber('T 0954/98'))
        x = AnalysisHelpers.AttributeFrequency(decisions)
        self.assertEqual(x['131'], 1)
        
    def test_articleFrequencyForBoard(self):        
        from Decisions.Analysers import AnalysisHelpers
        x = AnalysisHelpers.AttributeFrequencyForBoard('3.5.01')
        self.assertTrue(x['56'] > 1000)        

    def test_citationFrequency(self):
        from Decisions.DBProxy import DecisionModelProxy
        from Decisions.Analysers import AnalysisHelpers
        decisions = DecisionModelProxy.GetAllForBoard('3.1.01')
        x = AnalysisHelpers.CitationFrequency(decisions)
        y = {dec.CaseNumber: count for (dec, count) in x.items()}
        self.assertTrue(y['J 0005/80'] > 50)
        
    def test_citationFrequencyForBoard(self):        
        from Decisions.Analysers import AnalysisHelpers
        x = AnalysisHelpers.CitationFrequencyForBoard('3.5.01')
        y = {dec.CaseNumber: count for (dec, count) in x.items()}
        self.assertTrue(y['T 0441/92'] > 15)
