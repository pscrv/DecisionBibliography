from django.db.models import F
from django.core.exceptions import FieldDoesNotExist

import re

from DecisionsPlus.models import BibliographyBaseModel, BibliographyLanguageVersionModel, TextModel, CitationSupplementModel
from DecisionsPlus.Decision import DecisionProxy


#region private methods
def __getLanguageVersionListFromKeys(**kwargs):
    
    try:
        kw_dict = __splitKeywords(**kwargs)
    except FieldDoesNotExist:
        return []
    
    result = BibliographyLanguageVersionModel.objects.filter(**kw_dict)
    return result


def __splitKeywords(**kwargs):
    models = [BibliographyBaseModel, BibliographyLanguageVersionModel, TextModel, CitationSupplementModel]
        
    keyprefixes = {
        BibliographyBaseModel: 'BibliographyBase__',
        BibliographyLanguageVersionModel: '', 
        TextModel: 'TextModel__', 
        CitationSupplementModel: 'CitationSupplementModel__',
        }

    result = {}
    for key, value in kwargs.items():
        base = __getBaseFieldName(key)
        found = False
        for model in models:
            if found:
                continue
            if base in getattr(model, 'FieldNames'):
                found = True
                result[keyprefixes[model] + key] = value
        if not found:
            raise FieldDoesNotExist
    return result


def __getBaseFieldName(field):
    finder = re.compile(r'(.+)__')
    found = finder.match(field)
    return found.group(1) if found else field


def __toDecisionList(languageversions):
    result = [DecisionProxy(x) for x in languageversions]
    return result

    
def __countFromKeys(**kwargs):
    return __getLanguageVersionListFromKeys(**kwargs).count()
        

# Does this work?
def __getDistinctBibliograpyAttributeValueList(attribute):
    return list(__getLanguageVersionListFromKeys().values_list(attribute, flat = True).distinct())
    
#endregion
    

#region public methods  
def GetListFromKeywords(**kwargs):
    result = __getLanguageVersionListFromKeys(**kwargs)
    decisions = __toDecisionList(result)
    return decisions

    
def GetRepresentativeForCaseNumber(cn):
    decisions = GetListFromKeywords(CaseNumber = cn, DecisionLanguage =  F('BibliographyBase__ProcedureLanguage'))
    if len(decisions) > 0:
        return decisions[0]
    else:
        base = BibliographyBaseModel(CaseNumber = cn)
        lang = BibliographyLanguageVersionModel(BibliographyBase = base)
        decision = DecisionProxy(lang)
        return decision


def GetDecisionFromPrimaryKey(pk):
    result = BibliographyLanguageVersionModel.objects.filter(pk = pk).first()
    decision = DecisionProxy(result)
    return decision


def GetCitedCasesFromCaseNumber(cn):
    case = BibliographyLanguageVersionModel.objects.filter(BibliographyBase__CaseNumber = cn).first()
    if not case:
        return ''
    
    bibCited = {x.strip() for x in case.BibliographyBase.CitedCases.split(',') if x != ''}
    cited = bibCited
    
    supp = getattr(case, 'CitationSupplementModel', None)
    if supp is not None:
        bibBadCited = set(supp.CitedCases_notInDB.split(','))
        textCited = set(supp.TextCited_inDB.split(','))
        cited = set.union(bibCited.difference(bibBadCited), textCited)

    decisions = [GetRepresentativeForCaseNumber(x) for x in cited]
    return decisions

    
def GetCitingCasesFromCaseNumber(cn):
    case = BibliographyLanguageVersionModel.objects.filter(BibliographyBase__CaseNumber = cn).first()
    if not case:
        return ''

    supp = getattr(case, 'CitationSupplementModel', None)
    if supp is not None:
        bibCiting = set(supp.BibliographyCiting.split(','))
        textCiting = set(supp.TextCiting.split(','))
        resultSet = set.union(bibCiting, textCiting)
    else:
        bibCiting = BibliographyBaseModel.objects.filter(CitedCases__contains = cn)
        resultSet = {x.CaseNumber for x in bibCiting}
    
    resultSet.discard('')
    #resultString = ','.join(resultSet)
    decisions = [GetRepresentativeForCaseNumber(x) for x in resultSet]
    return decisions
        

def GetCitingCasesFromPK(pk):
    case = BibliographyLanguageVersionModel.objects.filter(pk = pk).first()
    if not case:
        return ''
    result = GetCitingCasesFromCaseNumber(case.BibliographyBase.CaseNumber)
    return result
   

def GetAllForBoard(board):
    result = __getLanguageVersionListFromKeys(Board = board, DecisionLanguage = F('BibliographyBase__ProcedureLanguage'))
    decisions = __toDecisionList(result)
    return decisions
   

def GetAllForBoardOrderedByDecisionDate(board):
    result = __getLanguageVersionListFromKeys(Board = board, DecisionLanguage = F('BibliographyBase__ProcedureLanguage'))
    result = result.order_by('BibliographyBase__DecisionDate')
    decisions = __toDecisionList(result)
    return decisions

    
def GetEarliest(howmany = 1):
    result = BibliographyBaseModel.objects.filter(
        ProcedureLanguage = F('LanguageModel__DecisionLanguage')
        ).order_by('DecisionDate')[:howmany]
    resultlangs = [x.LanguageModel.first() for x in result]
    decisions = __toDecisionList(resultlangs)
    return decisions
 
    
def GetLatest(howmany = 1):
    result = BibliographyBaseModel.objects.filter(
        ProcedureLanguage = F('LanguageModel__DecisionLanguage')
        ).order_by('-DecisionDate')[:howmany]
    resultlangs = [x.LanguageModel.first() for x in result]
    decisions = __toDecisionList(resultlangs)
    return decisions


def GetCasetypeCount(typeletter):
    results = BibliographyBaseModel.objects.filter(CaseNumber__startswith = typeletter)
    count = results.count()
    return count


def GetBibliographyCount():
    return BibliographyBaseModel.objects.count()


def GetTextCount():
    results = TextModel.objects.values_list('Bibliography__BibliographyBase__CaseNumber', flat = True).distinct()
    count = results.count()
    return count


def GetBoardList():
    result = list(BibliographyBaseModel.objects.values_list('Board', flat = True).distinct())
    return result


def GetBibliographyAttributeList():
    result = BibliographyBaseModel.FieldNames + BibliographyLanguageVersionModel.FieldNames
    return result


    #only used in AnalysisHelpers.GetAttributeFrequency
    # put that function here?
    # better to split such attributes into a list before returning?
def IsListAttribute(attribute):
    return attribute in {
        'Opponents',
        'Respondents',
        'IPC',
        'Articles',
        'Rules',
        'CitedCases',
        }   

#endregion
    