from decimal import Decimal

from app.models import BoardAnalysisModel
from app.DBProxy import DecisionModelProxy
from Analysers.BoardAnalysis import BoardAnalysis, NullBoardAnalysis

def SaveBoardAnalysisToDB(analysis):

        earlyList = [str(x.pk) for x in analysis.Early]
        earlySavable = ','.join(earlyList)

        lateList = [str(x.pk) for x in analysis.Late]
        lateSavable = ','.join(lateList)

        ipcString = __stringIntDecimalToString(analysis.IpcTop5)
        articleString = __stringIntDecimalToString(analysis.ArticleTop5)

        citationList = [(str(x.pk), y) for (x, y) in analysis.CitationTop5]
        citationString = __stringIntToString(citationList)
        
        dbAnalysis, created = BoardAnalysisModel.objects.get_or_create(Board = analysis.Board)
        dbAnalysis.Count = analysis.Count
        dbAnalysis.EarliestFive = earlySavable
        dbAnalysis.LatestFive = lateSavable
        dbAnalysis.IPC_TopFive = ipcString
        dbAnalysis.Article_TopFive = articleString
        dbAnalysis.Cited_TopFive = citationString
        dbAnalysis.save()


def GetBoardAnalysisFromDB(board):

    dbAnalysis, created = BoardAnalysisModel.objects.get_or_create(Board = board)
    if created:
        return NullBoardAnalysis

    citationList = __stringIntFromString(dbAnalysis.Cited_TopFive)

    analysis = BoardAnalysis(
         board = dbAnalysis.Board,
         count = dbAnalysis.Count,
         early = __decisionListFromPkString(dbAnalysis.EarliestFive),
         late = __decisionListFromPkString(dbAnalysis.LatestFive),
         ipcTop5 = __stringIntDecimalFromString(dbAnalysis.IPC_TopFive),
         articleTop5 = __stringIntDecimalFromString(dbAnalysis.Article_TopFive),
         citationTop5 = __pkValueToDecisionValue(citationList))

    return analysis


    
def __stringIntDecimalToString(tripleList):
    resultString = ''
    for (string, integer, decimal) in tripleList:
        resultString += string + ',' + str(integer) + ',' + str(decimal) + ';'
    return resultString

def __stringIntToString(pairList):
    resultString = ''
    for (string, integer) in pairList:
            resultString += string + ',' + str(integer) + ';'
    return resultString

def __stringIntFromString(string):
    if not string:
        return []
    resultList = []
    for pair in string.split(';'):
        if not pair:
            continue
        pairList = pair.split(',')
        resultList.append((pairList[0], int(pairList[1])))
    return resultList    

def __decisionListFromPkString(string):
    if not string:
        return []
    pkList = [int(x) for x in string.split(',')]
    result = []
    for pk in pkList:
        decision = DecisionModelProxy.GetDecisionFromPrimaryKey(pk)
        if decision:
            result.append(decision)
    return result

def __stringIntDecimalFromString(string):
    if not string:
        return []
    resultList = []
    for triple in string.split(';'):
        if not triple:
            continue
        tripleList = triple.split(',')
        resultList.append((tripleList[0], int(tripleList[1]), Decimal(tripleList[2])))
    return resultList    

def __pkValueToDecisionValue(pairs):
    result = []
    for (pk, value) in pairs:
        decision = DecisionModelProxy.GetDecisionFromPrimaryKey(pk)
        if decision:
            result.append((decision, value))
    return result
