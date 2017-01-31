
import datetime
from Decisions import DateHelpers
from Decisions.EpoSearchFacade import EpoSearchFacade
from Decisions.EpoConverter import EpoConverter
from Decisions.models import DecisionBibliographyModel, DecisionTextModel


class BibliographyGetter(object):    


    def GetAllForBoard(self, board):
        startyear = 9
        endyear = 10
        self.GetBoardFromYearToYear(board, startyear, endyear)

    def GetBoardFromYearToYear(self, board, fromyear, toyear):
        year = fromyear
        while year != toyear:
            yearstring = str(year)
            if year < 10:
                yearstring = '0' + yearstring
            self.GetYearForBoard(board, yearstring)
            if year == 99:
                year = 00
            else:
                year = year + 1


    def GetYearForBoard(self, board, yeardigitpair):

        searcher = EpoSearchFacade()
        converter = EpoConverter()
        try:
            response = searcher.SearchByBoardAndCaseYear(board, yeardigitpair)
            decs = converter.ResponseToDecisionList(response)
        except Exception as ex:
            t = type(ex)
            return
        self.__updateDB(decs)

               
    def GetAllForType(self, casetype):

        searcher = EpoSearchFacade()
        converter = EpoConverter()
        try:
            response = searcher.SearchByCaseType(casetype)
            decs = converter.ResponseToDecisionList(response)
        except Exception as ex:
            t = type(ex)
            return
        self.__updateDB(decs)
                        
               
                        


    def __updateDB(self, decisionlist):
        for case in decisionlist:
            inDB = DecisionBibliographyModel.objects.filter(
                CaseNumber = case.CaseNumber, 
                DecisionDate = case.DecisionDate,
                DecisionLanguage = case.DecisionLanguage
                ).first()

            if inDB:
                pass  # already have it
            else:
               case.save()



    

           


