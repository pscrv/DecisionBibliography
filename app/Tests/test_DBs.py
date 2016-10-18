"""
Unit tests
"""
import datetime
import django
from django.test import TestCase


class test_DecisionBibliographyModel(TestCase):
    
    @classmethod
    def setUpClass(cls):    
        super(test_DecisionBibliographyModel, cls).setUpClass()
        django.setup()
    
    
    def test_earliest(self):
        from app.models import DecisionBibliographyModel as DB
        item = DB.objects.order_by('DecisionDate').first()
        self.assertEqual(item.CaseNumber, 'J 0002/78')
        self.assertEqual(item.DecisionDate, datetime.date(1979, 3, 1))
        
    def test_latestUpTo1999(self):
        from app.models import DecisionBibliographyModel as DB
        item = DB.objects.order_by('-DecisionDate').first()
        self.assertEqual(item.CaseNumber, 'G 0001/97')
        self.assertEqual(item.DecisionDate, datetime.date(1999, 12, 10))
        
    def test_3501Eearliest(self):
        from app.models import DecisionBibliographyModel as DB
        item = DB.objects.FilterOnlyPrLanguage(Board = '3.5.01').order_by('DecisionDate').first()
        self.assertEqual(item.CaseNumber, 'T 0021/81')
        self.assertEqual(item.DecisionDate, datetime.date(1982, 9, 10))



class test_DecisionTextModel(TestCase):
     
    @classmethod
    def setUpClass(cls):    
        super(test_DecisionTextModel, cls).setUpClass()
        django.setup()    
    
    def test_earliest(self):
        from app.models import DecisionTextModel as textDB, DecisionBibliographyModel as bibDB
        dec = bibDB.objects.FilterOnlyPrLanguage(CaseNumber = 'J 0002/78')
        item = textDB.objects.filter(decision = dec).first()
        self.assertEqual(item.Reasons[0:33], 'Die Beschwerde richtet sich gegen')


class test_DecisionModelProxy(TestCase):

    @classmethod
    def setUpClass(cls):    
        super(test_DecisionModelProxy, cls).setUpClass()
        django.setup()

    def test_GetBoardList(self):
        from app.DBProxy import DecisionModelProxy
        boards = DecisionModelProxy.GetBoardList()
        self.assertEqual(len(boards), 21)

    
    def test_GetDistinctAttributeValueList(self):
        from app.DBProxy import DecisionModelProxy
        classes = DecisionModelProxy.GetDistinctAttributeValueList('IPC')
        applicants = DecisionModelProxy.GetDistinctAttributeValueList('Applicant')
        self.assertEqual(len(classes), 2631)
        self.assertEqual(len(applicants), 2689)


        
class test_DBAnalyser(TestCase):

    @classmethod
    def setUpClass(cls):    
        super(test_DBAnalyser, cls).setUpClass()
        django.setup()


    def test_GetBoardAnalysis(self):
        from Analysers import Persistent
        board = '3.5.01'
        analyser = Persistent.PersistentAnalyser()
        analysis = analyser.GetBoardAnalysis(board)
        analyser.AnalyseBoard(board)
        analysis = analyser.GetBoardAnalysis(board)


    def test_timelineFromString(self):
        from Analysers.Timelines import TimelineAnylser
        analyser = TimelineAnylser()
        string = "1992/02/01::13;1997/03/31::2;"
        timeline = analyser.GetBoardTimelineFromString(string)

        date1 = datetime.date(1992, 2, 1)
        date2 = datetime.date(1997, 3, 31)
        self.assertEqual(timeline[date1], 13)
        self.assertEqual(timeline[date2], 2)

    def test_ipcFrequency(self):
        from app.DBProxy import DecisionModelProxy
        from Analysers import AnalysisHelpers
        decisions = (DecisionModelProxy.GetBibliographyFiltered(CaseNumber = 'G 0001/97'))
        x = AnalysisHelpers.IpcFrequency(decisions)
        self.assertEqual(x['G04B 37/16'], 1)

    def test_ipcFrequencyForBoard(self):        
        from Analysers import AnalysisHelpers
        x = AnalysisHelpers.IpcFrequencyForBoard('3.5.01')
        self.assertEqual(x['H04N 1/46'], 2)

    def test_articleFrequency(self):
        from app.DBProxy import DecisionModelProxy
        from Analysers import AnalysisHelpers
        decisions = (DecisionModelProxy.GetBibliographyFiltered(CaseNumber = 'T 0954/98'))
        x = AnalysisHelpers.ArticleFrequency(decisions)
        self.assertEqual(x['131'], 1)
        
    def test_articleFrequencyForBoard(self):        
        from Analysers import AnalysisHelpers
        x = AnalysisHelpers.ArticleFrequencyForBoard('3.5.01')
        self.assertEqual(x['56'], 237)
        

    def test_citationFrequency(self):
        from app.DBProxy import DecisionModelProxy
        from Analysers import AnalysisHelpers
        decisions = DecisionModelProxy.GetAllForBoard('3.1.01')
        x = AnalysisHelpers.CitationFrequency(decisions)
        y = {dec.CaseNumber: count for (dec, count) in x.items()}
        self.assertEqual(y['J 0005/80'], 23)
        
    def test_citationFrequencyForBoard(self):        
        from Analysers import AnalysisHelpers
        x = AnalysisHelpers.CitationFrequencyForBoard('3.5.01')
        y = {dec.CaseNumber: count for (dec, count) in x.items()}
        self.assertEqual(y['T 0441/92'], 2)
