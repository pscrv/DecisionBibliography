from django.db.models import F

from Decisions.models import DecisionBibliographyModel, NullBibliographyModel, DecisionTextModel, NullTextModel
from Decisions.Decision import DecisionProxy


class DecisionModelProxy():


    #region private methods
    def __getDecisionFromBibliographyKeys(**kwargs):
        bibliographies = DecisionBibliographyModel.objects.filter(**kwargs)
        if bibliographies.count() > 1:
            bibliographies = bibliographies.filter(DecisionLanguage = F('ProcedureLanguage'))
        bibliography = bibliographies.first()
        if bibliography is None:
            casenumber = kwargs.get('CaseNumber', 'X xxxx/xx')
            return NullBibliographyModel(casenumber)
        text = DecisionModelProxy.__getTextFromBibliography(bibliography)
        return DecisionProxy(bibliography, text)

    
    def __getDecisionListFromBibliographyKeys(onlyprocedurelanguage = False, orderfield = None, howmany = None, **kwargs):
        bibliographies = DecisionBibliographyModel.objects.filter(**kwargs)
        if orderfield:
            bibliographies = bibliographies.order_by(orderfield)
        if onlyprocedurelanguage:
            bibliographies = bibliographies.filter(DecisionLanguage = F('ProcedureLanguage'))
        if howmany:
            bibliographies = bibliographies[:howmany]
        decisions = [
            DecisionProxy(x, DecisionModelProxy.__getTextFromBibliography(x))
            for x in bibliographies
            ]
        return decisions


    def __countFromBibliographyKey(**kwargs):
        return DecisionBibliographyModel.objects.filter(**kwargs).count()


    def __getTextFromBibliography(bibliography):        
        try:
            text = DecisionTextModel.objects.get(Bibliography = bibliography)
        except DecisionTextModel.DoesNotExist:
            text = NullTextModel()
            text.Bibliography = bibliography
        return text


    def __getDistinctBibliograpyAttributeValueList(attribute):
        return list(DecisionBibliographyModel.objects.values_list(attribute, flat = True).distinct())
    
    #endregion
    

    #region public methods  
    def GetListFromBibliographyKeywords(**kwargs):
        return DecisionModelProxy.__getDecisionListFromBibliographyKeys(**kwargs)


    def GetListFromTextKeywords(**kwargs):
        result_qset = DecisionTextModel.objects.filter(**kwargs)
        return [DecisionProxy(t.Bibliography, t) for t in result_qset]

    
    def GetRepresentativeForCaseNumber(cn):
        return DecisionModelProxy.__getDecisionFromBibliographyKeys(CaseNumber = cn)
    

    def GetDecisionFromPrimaryKey(pk):
        return DecisionModelProxy.__getDecisionFromBibliographyKeys(pk = pk)


    def GetListFromCaseNumber(cn):
        return DecisionModelProxy.__getDecisionListFromBibliographyKeys(CaseNumber = cn)
    
        
    def GetCitingCasesFromCaseNumber(cn):
        result = DecisionModelProxy.__getDecisionListFromBibliographyKeys(CitedCases__contains=cn, onlyprocedurelanguage = True)
        return result

    
    def GetAllForBoard(board):
        return DecisionModelProxy.__getDecisionListFromBibliographyKeys(Board = board, onlyprocedurelanguage = True)

    
    def GetAllForBoardOrderedByDecisionDate(board):
        return DecisionModelProxy.__getDecisionListFromBibliographyKeys(Board = board, onlyprocedurelanguage = True, orderfield = 'DecisionDate')

    
    def GetEarliest(howmany = 1):
        return DecisionModelProxy.__getDecisionListFromBibliographyKeys(onlyprocedurelanguage = True, orderfield = 'DecisionDate', howmany = howmany)
    
    
    def GetLatest(howmany = 1):
        return DecisionModelProxy.__getDecisionListFromBibliographyKeys(onlyprocedurelanguage = True, orderfield = '-DecisionDate', howmany = howmany)


    def GetCasetypeCount(typeletter):
        return DecisionModelProxy.__countFromBibliographyKey(CaseNumber__startswith = typeletter)
    

    def GetBibliographyCount():
        return DecisionBibliographyModel.objects.count()

    
    def GetTextCount():
        return DecisionTextModel.objects.count()


    def GetBoardList():
        return DecisionModelProxy.__getDistinctBibliograpyAttributeValueList('Board')


    def IsListAttribute(attribute):
        return DecisionBibliographyModel.objects.IsListAttribute(attribute)


    def GetBibliographyAttributeList():
        return vars(DecisionBibliographyModel)
    #endregion
    