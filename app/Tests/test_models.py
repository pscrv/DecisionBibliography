"""
Unit tests for epoConverter
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