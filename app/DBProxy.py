from abc import ABC, abstractmethod

from django.db.models import F
from app.models import DecisionBibliographyModel, DecisionTextModel

class DBProxy(ABC):
    """abstract base class for DB access"""
    
    #region Bibliography getters
    @abstractmethod
    def GetFiltered(**kwargs):
        pass

    @abstractmethod
    def GetRepresentativeForCaseNumber(cn):
        pass

    @abstractmethod
    def GetDefaultAndOthersFromPrimaryKey(pk):
        pass

    @abstractmethod
    def GetDefaultAndOthersFromCaseNumber(cn):
        pass

    @abstractmethod
    def GetCitingCasesFromCaseNumber(cn):
        pass

    @abstractmethod
    def GetAllOrderedByDecisionDate():
        pass
    
    @abstractmethod
    def GetAllForBoard(board):
        pass

    @abstractmethod
    def GetAllForBoardOrderedByDecisionDate(board):
        pass
    
    @abstractmethod
    def GetAllInDateRange(startDate, endDate):
        pass
        
    @abstractmethod
    def GetEarliestByDecisionDate(howmany = 1):
        pass
    
    @abstractmethod
    def GetLatestByDecisionDate(howmany = 1):
        pass
    #endregion

    
    #region Text getters
    @abstractmethod
    def GetTextFromDecision(decision):
        pass
    
    @abstractmethod
    def GetErrorText():
        pass
    #endregion

        
    #region Bibliography metadata
    @abstractmethod
    def GetCasetypeCount(typeletter):
        pass
    
    @abstractmethod
    def GetBibliographyCount():
        pass
    
    @abstractmethod
    def GetIsListAttribute(attribute):
        pass

    @abstractmethod
    def GetBibliographyAttributeList():
        return vars(DecisionBibliographyModel)
    #endregion
    
    #region Text metadata
    @abstractmethod
    def GetTextCount():
        pass
    #endregion


class DecisionModelProxy(DBProxy):
    """proxy class for accessing DecisionBibliographyModel and DecisionTextModel """

    #region Bibliography getters
    def GetFiltered(**kwargs):
        return DecisionBibliographyModel.objects.FilterOnlyPrLanguage(**kwargs)


    def GetRepresentativeForCaseNumber(cn):
        return  DecisionBibliographyModel.objects.FilterOnlyPrLanguage(CaseNumber=cn).first()

    def GetDefaultAndOthersFromPrimaryKey(pk):
        default = DecisionBibliographyModel.objects.filter(pk = pk).first()
        decisionList = DecisionBibliographyModel.objects.filter(CaseNumber = default.CaseNumber)
        others = decisionList.exclude(pk = default.pk)
        return default, others


    def GetDefaultAndOthersFromCaseNumber(cn):
        decisionList = DecisionBibliographyModel.objects.filter(CaseNumber = cn)
        default = decisionList.filter(DecisionLanguage =  F('ProcedureLanguage')).first()
        others = decisionList.exclude(pk = default.pk)
        return default, others

    def GetCitingCasesFromCaseNumber(cn):
        return DecisionBibliographyModel.objects.FilterOnlyPrLanguage(CitedCases__contains=cn).all()

    def GetAllOrderedByDecisionDate():
        return DecisionBibliographyModel.objects.order_by('DecisionDate')
    
    def GetAllForBoard(board):
        return DecisionBibliographyModel.objects.FilterOnlyPrLanguage(Board = board)

    def GetAllForBoardOrderedByDecisionDate(board):
        return DecisionBibliographyModel.objects.FilterOnlyPrLanguage(Board = board).order_by('DecisionDate')

    def GetAllInDateRange(startDate, endDate):
        return DecisionBibliographyModel.objects.FilterOnlyPrLanguage(DecisionDate__range = (startDate, endDate))

    def GetEarliestByDecisionDate(howmany = 1):
        return DecisionBibliographyModel.objects.order_by('DecisionDate')[:howmany]

    def GetLatestByDecisionDate(howmany = 1):
        return DecisionBibliographyModel.objects.order_by('-DecisionDate')[:howmany]
    #endregion

    #region Text getters
    def GetTextFromDecision(decision):
        return DecisionTextModel.objects.filter(decision = decision).first()

    def GetErrorText():
        return  DecisionTextModel(
            FactsHeader = "Decision text unavailable.",
            Facts = "",
            ReasonsHeader = "Decision text unavailable.",
            Reasons = "",
            OrderHeader = "Decision text unavailable.",
            Order = "")
    #endregion

    #region Bibliography meta
    def GetCasetypeCount(typeletter):
         return DecisionBibliographyModel.objects.filter(CaseNumber__startswith=typeletter).count()     

    def GetBibliographyCount():
        return DecisionBibliographyModel.objects.count();

    def GetIsListAttribute(attribute):
        return DecisionBibliographyModel.objects.IsListAttribute(attribute)

    def GetBibliographyAttributeList():
        return vars(DecisionBibliographyModel)
    #endregion

    #region Text meta
    def GetTextCount():
        return DecisionTextModel.objects.count();
    #endregion