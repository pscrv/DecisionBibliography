from abc import ABC, abstractmethod

from django.db.models import F, Q
from Decisions.models import DecisionBibliographyModel, DecisionTextModel, NullTextModel
from Decisions.Decision import DecisionProxy


class DecisionModelProxy():

    #region Adding here

    #private methods
    def __getDecisionFromBibliographyKeys(**kwargs):
        bibliographies = DecisionBibliographyModel.objects.filter(**kwargs)
        if bibliographies.count() > 1:
            bibliographies = bibliographies.filter(DecisionLanguage = F('ProcedureLanguage'))
        bibliography = bibliographies.first()
        if bibliography is None:
            return None
        text = DecisionModelProxy.__getTextFromBibliography(bibliography)
        return DecisionProxy(bibliography, text)

    
    def __getDecisionListFromBibliographyKeys(**kwargs):
        bibliographies = DecisionBibliographyModel.objects.filter(**kwargs)
        decisions = [
            DecisionProxy(x, DecisionModelProxy.__getTextFromBibliography(x))
            for x in bibliographies
            ]
        return decisions



        text = DecisionModelProxy.__getTextFromBibliography(bibliography)
        return DecisionProxy(bibliography, text)


    def __getTextFromBibliography(bibliography):        
        try:
            text = DecisionTextModel.objects.get(Bibliography = bibliography)
        except DecisionTextModel.DoesNotExist:
            text = NullTextModel()
            text.Bibliography = bibliography
        return text

    #endregion
    
      
    def GetFilteredOnBibliographyKeywords(**kwargs):
        result_qset = DecisionBibliographyModel.objects.filter(**kwargs)
        result_list = []
        for bibliography in result_qset:
            try:
                text = DecisionTextModel.objects.get(Bibliography = bibliography)
            except DecisionTextModel.DoesNotExist:
                text = NullTextModel()
                text.Bibliography = bibliography

            result_list.append(DecisionProxy(bibliography, text))

        return result_list


    def GetFilteredOnTextKeywords(**kwargs):
        result_qset = DecisionTextModel.objects.filter(**kwargs)
        return [DecisionProxy(t.Bibliography, t) for t in result_qset]

    
    def GetRepresentativeForCaseNumber(cn):
        return DecisionModelProxy.__getDecisionFromBibliographyKeys(CaseNumber = cn)
    
    def GetDecisionFromPrimaryKey(pk):
        return DecisionModelProxy.__getDecisionFromBibliographyKeys(pk = pk)


    def GetDecisionListFromCaseNumber(cn):
        result = DecisionModelProxy.__getDecisionListFromBibliographyKeys(CaseNumber = cn)
        return result
        #decisionList = DecisionBibliographyModel.objects.filter(CaseNumber = cn)
        #return decisionList
    
    #endegion

    #region Bibliography getters

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
    def GetTextFromBibliography(decision):
        return DecisionTextModel.objects.filter(Bibliography = decision).first()

    def GetErrorText():
        return  DecisionTextModel(
            FactsHeader = "Decision text unavailable.",
            Facts = "",
            ReasonsHeader = "Decision text unavailable.",
            Reasons = "",
            OrderHeader = "Decision text unavailable.",
            Order = "")

    #def GetTextsFiltered(**kwargs):
    #    return DecisionTextModel.objects.filter(**kwargs)
    #endregion

    #region Bibliography meta
    def GetCasetypeCount(typeletter):
        return DecisionBibliographyModel.objects.filter(CaseNumber__startswith=typeletter).count()     
          
        # no longer used?
        # check and delete if possible
    def GetBibliographyCount():
        return DecisionBibliographyModel.objects.count()

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

    def ExtractCasenumbersFromText(decision):
        decisionText = DecisionModelProxy.GetTextFromBibliography(decision)
        fullText = decisionText.Facts + decisionText.Reasons + decisionText.Order

        import re
        finder = re.compile(r'([DGJRTW])\s*(\d+)/(\d+)') #newlines are unlikely to matter
        found = re.finditer(finder, fullText)

        from app.Formatters import formatCaseNumber
        numbers = set(formatCaseNumber(x.group(0)) for x in found)
        return numbers

    #endregion
