import django
from django.test import TestCase

from datetime import datetime


class DecisionPlusProxy(TestCase):
    """Tests for the application views."""

    if django.VERSION[:2] >= (1, 7):
        # Django 1.7 requires an explicit setup() when running tests in PTVS
        @classmethod
        def setUpClass(cls):
            super().setUpClass()
            django.setup()
            
    
    def test_GetListFromBadField(self):
        from DecisionsPlus import DecisionModelProxy
        results = DecisionModelProxy.GetListFromKeywords(BadFieldName = '   ')
        self.assertEqual(len(results), 0)


    def test_GetListFromCaseNumber(self):
        from DecisionsPlus import DecisionModelProxy
        casenumber = 'T 0641/00'
        casedate = datetime.strptime('26.09.2002', '%d.%m.%Y').date()
        results = DecisionModelProxy.GetListFromKeywords(CaseNumber = casenumber)
        self.assertEqual(len(results), 3)
        for res in results:
            self.assertEqual(res.CaseNumber, casenumber)
            self.assertEqual(res.DecisionDate, casedate)

    
    def test_GetListFromBadCaseNumber(self):
        from DecisionsPlus import DecisionModelProxy
        casenumber = 'T zzzz/zz'
        results = DecisionModelProxy.GetListFromKeywords(CaseNumber = casenumber)
        self.assertEqual(len(results), 0)

            
    def test_GetListFromDate(self):
        from DecisionsPlus import DecisionModelProxy
        casedate = datetime.strptime('26.09.2002', '%d.%m.%Y').date()
        results = DecisionModelProxy.GetListFromKeywords(DecisionDate = casedate)
        self.assertGreaterEqual(len(results), 13)
        for res in results:
            self.assertEqual(res.DecisionDate, casedate)
            
    def test_GetListFromBadDate(self):
        from DecisionsPlus import DecisionModelProxy
        casedate = datetime.strptime('01.01.1821', '%d.%m.%Y').date()
        results = DecisionModelProxy.GetListFromKeywords(DecisionDate = casedate)
        self.assertEqual(len(results), 0)
        

    def test_GetListFromApplicant__contains(self):
        from DecisionsPlus import DecisionModelProxy
        appl = 'COMVIK'
        results = DecisionModelProxy.GetListFromKeywords(Applicant__contains = appl)
        self.assertEqual(len(results), 3)
        for res in results:
            self.assertIn(appl, res.Applicant)
            
    def test_GetListFromBadApplicant__contains(self):
        from DecisionsPlus import DecisionModelProxy
        appl = 'zzzzzzzz'
        results = DecisionModelProxy.GetListFromKeywords(Applicant__contains = appl)
        self.assertEqual(len(results), 0)

        
    def test_GetListFromTitle__contains(self):
        from DecisionsPlus import DecisionModelProxy
        word = 'identities'
        results = DecisionModelProxy.GetListFromKeywords(Title__contains = word)
        for res in results:
            self.assertIn(word, res.Title)
            
    def test_GetListFromBadTitle__contains(self):
        from DecisionsPlus import DecisionModelProxy
        word = 'zzzzzzzz####'
        results = DecisionModelProxy.GetListFromKeywords(Title__contains = word)
        self.assertEqual(len(results), 0)

                
    def test_GetListFromFacts__contains(self):
        from DecisionsPlus import DecisionModelProxy
        word = 'identities'
        results = DecisionModelProxy.GetListFromKeywords(Facts__contains = word)
        for res in results:
            self.assertIn(word, ' '.join(res.Facts))
            
    def test_GetListFromBadFacts__contains(self):
        from DecisionsPlus import DecisionModelProxy
        word = 'zzzzzzzz####'
        results = DecisionModelProxy.GetListFromKeywords(Facts__contains = word)
        self.assertEqual(len(results), 0)

        
    def test_GetRepresenttiveFromCaseNumber(self):
        from DecisionsPlus import DecisionModelProxy
        cn = 'T 0641/00'
        result = DecisionModelProxy.GetRepresentativeForCaseNumber(cn)
        self.assertEqual(result.CaseNumber, cn)
            
    def test_GetRepresenttiveFromBadCaseNumber(self):
        from DecisionsPlus import DecisionModelProxy
        cn = 'zzzzzzzz####'
        result = DecisionModelProxy.GetRepresentativeForCaseNumber(cn)
        self.assertEqual(result.CaseNumber, cn)

        
    def test_GetDecisionFromPk(self):
        from DecisionsPlus import DecisionModelProxy
        cn = 'T 0641/00'
        decision = DecisionModelProxy.GetRepresentativeForCaseNumber(cn)
        result = DecisionModelProxy.GetDecisionFromPrimaryKey(decision.pk)
        self.assertEqual(result.pk, decision.pk)
            
    def test_GetDecsionFromBadPk(self):
        from DecisionsPlus import DecisionModelProxy
        pk = -1
        result = DecisionModelProxy.GetDecisionFromPrimaryKey(pk)
        self.assertEqual(result.CaseNumber, 'Unknown case')


    def test_GetCitedFromCaseNumber(self):
        from DecisionsPlus import DecisionModelProxy
        cn = 'T 0641/00'
        result = DecisionModelProxy.GetCitedCasesFromCaseNumber(cn)
        result_cns = [x.CaseNumber for x in result]
        self.assertTrue('T 0026/81' in result_cns)
        self.assertTrue('T 0026/86' in result_cns)
        self.assertTrue('T 0931/95' in result_cns)

    def test_GetCitingFromCaseNumber(self):
        from DecisionsPlus import DecisionModelProxy
        cn = 'T 0641/00'
        result = DecisionModelProxy.GetCitingCasesFromCaseNumber(cn)
        result_cns = [x.CaseNumber for x in result]
        self.assertTrue('G 0003/08' in result_cns)
        self.assertTrue('T 1421/08' in result_cns)
        self.assertTrue('T 1769/10' in result_cns)
            
        
    def test_GetCitingFromPk(self):
        from DecisionsPlus import DecisionModelProxy
        from DecisionsPlus.models import BibliographyLanguageVersionModel
        cn = 'T 0641/00'
        case = BibliographyLanguageVersionModel.objects.filter(BibliographyBase__CaseNumber = cn).first()
        result = DecisionModelProxy.GetCitingCasesFromPK(case.pk)
        result_cns = [x.CaseNumber for x in result]
        self.assertTrue('G 0003/08' in result_cns)
        self.assertTrue('T 1421/08' in result_cns)
        self.assertTrue('T 1769/10' in result_cns)

                
    def test_GetAllForBoard(self):
        from DecisionsPlus import DecisionModelProxy
        board = '3.5.01'
        result = DecisionModelProxy.GetAllForBoard(board)
        casenumberlist = [x.CaseNumber for x in result]
        casenumberset = set(casenumberlist)
        self.assertTrue('T 0641/00' in casenumberset)
        self.assertTrue('T 1411/08' in casenumberset)
        for res in result:
            self.assertEqual(res.Board, board)
            
        
    def test_GetAllForBoardOrderedByDecisionDate(self):
        from DecisionsPlus import DecisionModelProxy
        board = '3.5.07'
        result = DecisionModelProxy.GetAllForBoardOrderedByDecisionDate(board)
        for index in range(0, len(result) - 1):
            this = result[index].DecisionDate
            next = result[index + 1].DecisionDate
            self.assertTrue(this <= next, 'this {} not <= next {}'.format(this, next))
            
        
    def test_GetEarliest(self):
        from DecisionsPlus import DecisionModelProxy
        result = DecisionModelProxy.GetEarliest(3)
        for index in range(0, 2):
            this = result[index].DecisionDate
            next = result[index + 1].DecisionDate
            self.assertTrue(this <= next, 'this {} not <= next {}'.format(this, next))
        self.assertEqual(result[0].DecisionDate.year, 1979)

                 
    def test_GetLatest(self):
        from DecisionsPlus import DecisionModelProxy
        result = DecisionModelProxy.GetLatest(3)
        for index in range(0, 2):
            this = result[index].DecisionDate
            next = result[index + 1].DecisionDate
            self.assertTrue(this >= next, 'this {} not <= next {}'.format(this, next))
        self.assertEqual(result[0].DecisionDate.year, 2017)

        
    def test_GetCasetypeCount(self):
        from DecisionsPlus import DecisionModelProxy
        result = DecisionModelProxy.GetCasetypeCount('G')
        self.assertGreaterEqual(result, 99)  #up to January 2017

        
    def test_GetBibliographyCount(self):
        from DecisionsPlus import DecisionModelProxy
        result = DecisionModelProxy.GetBibliographyCount()
        self.assertGreaterEqual(result, 32500)  #up to January 2017

        
    def test_GetTextCount(self):
        from DecisionsPlus import DecisionModelProxy
        result = DecisionModelProxy.GetTextCount()
        self.assertGreaterEqual(result, 1100)  #up to January 2017
        
        
    def test_GetBoardList(self):
        from DecisionsPlus import DecisionModelProxy
        result = DecisionModelProxy.GetBoardList()
        self.assertTrue('3.5.01' in result)
        self.assertTrue('3.4.02' in result)
        self.assertTrue('EBA' in result)
        
        
    def test_GetBibliographyAttributeList(self):
        from DecisionsPlus import DecisionModelProxy
        result = DecisionModelProxy.GetBibliographyAttributeList()
        self.assertTrue('CaseNumber' in result)
        self.assertTrue('Applicant' in result)
        self.assertFalse('Facts' in result)
        

    def test_IsListAttribute(self):
        from DecisionsPlus import DecisionModelProxy
        self.assertTrue(DecisionModelProxy.IsListAttribute('Opponents'))
        self.assertTrue(DecisionModelProxy.IsListAttribute('IPC'))
        self.assertFalse(DecisionModelProxy.IsListAttribute('CaseNumber'))
        
        
                
        




