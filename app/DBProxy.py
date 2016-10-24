from abc import ABC, abstractmethod

import operator
from functools import reduce
from django.db.models import F, Q
from app.models import DecisionBibliographyModel, DecisionTextModel

class DBProxy(ABC):
    """abstract base class for DB access"""
    
    #region Bibliography getters
    @abstractmethod
    def GetBibliographyFiltered(**kwargs):
        pass

    @abstractmethod
    def GetRepresentativeForCaseNumber(cn):
        pass

    @abstractmethod
    def GetDecisionFromPrimaryKey(pk):
        pass

    @abstractmethod
    def GetDecisionListFromPrimaryKey(pk):
        pass

    @abstractmethod
    def GetDecisionListFromCaseNumber(cn):
        pass

    @abstractmethod
    def GetDecisionListFromTextSearchANDTermList(termList):
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

    @abstractmethod
    def GetAttributeValueAsList(attribute):
        pass
    #endregion

    
    #region Text getters
    @abstractmethod
    def GetTextFromDecision(decision):
        pass
    
    @abstractmethod
    def GetErrorText():
        pass

    @abstractmethod
    def GetTextsFiltered(self, **kwargs):
        pass
    #endregion

        
    #region Bibliography metadata
    @abstractmethod
    def GetCasetypeCount(typeletter):
        pass
        
        # no longer used?
        # check and delete if possible
    @abstractmethod
    def GetBibliographyCount():
        pass
        
    @abstractmethod
    def GetDistinctBibliographiesCount():
        pass

    @abstractmethod
    def GetDistinctAttributeValueList(attribute):
        pass

    @abstractmethod
    def GetBoardList():
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
    def GetBibliographyFiltered(**kwargs):
        return DecisionBibliographyModel.objects.FilterOnlyPrLanguage(**kwargs)


    def GetRepresentativeForCaseNumber(cn):
        return  DecisionBibliographyModel.objects.FilterOnlyPrLanguage(CaseNumber=cn).first()

    def GetDecisionFromPrimaryKey(pk):
        return DecisionBibliographyModel.objects.filter(pk = pk).first()

    def GetDecisionListFromPrimaryKey(pk):
        default = DecisionBibliographyModel.objects.filter(pk = pk).first()
        decisionList = DecisionBibliographyModel.objects.filter(CaseNumber = default.CaseNumber)
        return decisionList


    def GetDecisionListFromCaseNumber(cn):
        decisionList = DecisionBibliographyModel.objects.filter(CaseNumber = cn)

    # Only used in IssueAnalyser
    # Experiment
    # Candidate for deletion
    def GetDecisionListFromTextSearchANDTermList(termList):
        factsResults = DecisionTextModel.objects.filter(reduce(operator.and_, (Q(Facts__contains = x) for x in termList)))
        reasonsResults = DecisionTextModel.objects.filter(reduce(operator.and_, (Q(Reasons__contains = x) for x in termList)))
        orderResults = DecisionTextModel.objects.filter(reduce(operator.and_, (Q(Order__contains = x) for x in termList)))
        return factsResults | reasonsResults | orderResults
        return decisionList

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
        return DecisionBibliographyModel.objects.FilterOnlyPrLanguage().order_by('DecisionDate')[:howmany]

    def GetLatestByDecisionDate(howmany = 1):
        return DecisionBibliographyModel.objects.FilterOnlyPrLanguage().order_by('-DecisionDate')[:howmany]

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

    def GetTextsFiltered(**kwargs):
        return DecisionTextModel.objects.filter(**kwargs)
    #endregion

    #region Bibliography meta
    def GetCasetypeCount(typeletter):
        return DecisionBibliographyModel.objects.filter(CaseNumber__startswith=typeletter).count()     
          
        # no longer used?
        # check and delete if possible
    def GetBibliographyCount():
        return DecisionBibliographyModel.objects.count

    def GetDistinctBibliographiesCount():
        return DecisionBibliographyModel.objects.FilterOnlyPrLanguage().count()

    def GetDistinctAttributeValueList(attribute):
        return list(DecisionBibliographyModel.objects.values_list(attribute, flat = True).distinct())

    def GetBoardList():
        return list(DecisionBibliographyModel.objects.values_list('Board', flat = True).distinct())

    def GetIsListAttribute(attribute):
        return DecisionBibliographyModel.objects.IsListAttribute(attribute)

    def GetBibliographyAttributeList():
        return vars(DecisionBibliographyModel)
    #endregion

    #region Text meta
    def GetTextCount():
        return DecisionTextModel.objects.count()
    #endregion
