
import datetime
from . EpoSearchFacade import EpoSearchFacade
from . EpoConverter import EpoConverter
from . models import DecisionBibliographyModel, DecisionTextModel
from . import DateHelpers


class BibliographyGetter(object):    

    def GetAll(self):
        startYear = 1979
        startMonth = 1
        startDate = datetime(startYear, startMonth, 1)

        now = datetime.datetime.now()
        endDate = (now - datetime.timedelta(days = now.day)).date() # last day of previous month
        Get_FromDate_ToDate(startDate, endDate)
        
        next_month = dt.replace(day=28) + datetime.timedelta(days=4)   # enough to get to the next month, no matter where we start
        return next_month - datetime.timedelta(days=next_month.day)

    def Get_FromDate_ToDate(self, start:datetime, end:datetime):
        currentDate = start
        while currentDate <= end:
            self._getOneMonth(currentDate)
            currentDate = DateHelpers.FirstOfNextMonth(currentDate)
 
    def _getOneMonth(self, date):
        startDate = datetime.date(date.year, date.month, 1)
        #endDate = self._endOfMonth(startDate)
        endDate = DateHelpers.EndOfThisMonth(startDate)
        searcher = EpoSearchFacade()
        converter = EpoConverter()

        try:
            response = searcher.SearchByDate(startDate, endDate)
            decs = converter.ResponseToDecisionList(response)
        except Exception as ex:
            t = type(ex)      
            return
        
        for case in decs:
            inDB = DecisionBibliographyModel.objects.filter(
                CaseNumber = case.CaseNumber, 
                DecisionDate = case.DecisionDate,
                DecisionLanguage = case.DecisionLanguage
                ).first()

            if inDB:
                pass  # already have it
            else:
                case.save()


class TextGetter(object):

    def Get_Text(self, decision):
        searcher = EpoSearchFacade()
        converter = EpoConverter()
        
        try:
            response = searcher.SearchDecisionText(self.__getTextLink(decision))
            decisionText = converter.ResponseToDecisionText(response)
            decisionText.decision = decision
            decisionText.Language = decision.ProcedureLanguage
        except Exception as ex:
            t = type(ex)      
            return None

        inDB = DecisionTextModel.objects.filter(
                decision = decision,
                Language = decision.ProcedureLanguage).first()

        if inDB:
            pass  # already here
        else:
            decisionText.save();

        return decisionText


    def __getTextLink(self, decision):
        language = decision.ProcedureLanguage
        if language == 'DE':
            link = decision.LinkDE
        elif language == 'EN':
            link = decision.LinkEN
        elif language == 'FR':
            link = decision.LinkFR
        else:
            link = None
        return link
           


