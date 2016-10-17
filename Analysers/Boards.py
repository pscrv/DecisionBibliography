import re
from decimal import Decimal
from app.DBProxy import DecisionModelProxy
from Analysers import AnalysisHelpers
#from Analysers.AnalysisHelpers import IpcFrequencyForBoard, ArticleFrequencyForBoard, CitationFrequencyForBoard


class BoardAnalyser(object):

    def __init__(self):
        self.__cache = {}


    def GetBoardAnalysis(self, board):
        if board in self.__cache:
            return self.__cache[board]

        analysis = self.__analyseBoard(board)
        self.__cache[board] = analysis
        return analysis
    
    def GetSavableBoardAnalysis(self, board):
        analysis = self.GetBoardAnalysis(board)

        earlyList = [str(x.pk) for x in analysis['early']]
        earlySavable = ','.join(earlyList)

        lateList = [str(x.pk) for x in analysis['late']]
        lateSavable = ','.join(lateList)

        ipcString = self.__stringIntDecimalToString(analysis['ipctop'])
        articleString = self.__stringIntDecimalToString(analysis['articletop'])

        citationList = [(str(x.pk), y) for (x, y) in analysis['citationtop']]
        citationString = self.__stringIntToString(citationList)

        result =  {
            'board': board,
            'count': analysis['count'], 
            'early': earlySavable, 
            'late': lateSavable, 
            'ipctop': ipcString,  
            'articletop': articleString, 
            'citationtop': citationString
            }

        return result

    def ParseSavableBoardAnalysis(self, savableAnalysis):
        
        citationList = self.__stringIntFromString(savableAnalysis['citationtop'])

        result =  {
            'board': savableAnalysis['board'],
            'count': savableAnalysis['count'], 
            'early': self.__decisionListFromPkString(savableAnalysis['early']), 
            'late': self.__decisionListFromPkString(savableAnalysis['late']), 
            'ipctop': self.__stringIntDecimalFromString(savableAnalysis['ipctop']), 
            'articletop': self.__stringIntDecimalFromString(savableAnalysis['articletop']), 
            'citationtop': self.__pkValueToDecisionValue(citationList),
            }

        return result


    def __analyseBoard(self, board):        
        boardDecisions = DecisionModelProxy.GetAllForBoardOrderedByDecisionDate(board)
        count = boardDecisions.count()
        early = boardDecisions[:5]
        if count >= 5:
            late = boardDecisions[count-5:]
        else:
            late = boardDecisions

        ipcTop5 = AnalysisHelpers.IpcMainFrequencyForBoard_TopN_withPercentage(board, 5, count)
        articleTop5 = AnalysisHelpers.ArticleFrequencyForBoard_TopN_withPercentage(board, 5, count)
        citationTop5 = AnalysisHelpers.ArticleFrequencyForBoard_TopN(board, 5)

        result =  {
            'board': board,
            'count': count, 
            'early': early, 
            'late': late, 
            'ipctop': ipcTop5, 
            'articletop': articleTop5, 
            'citationtop': citationTop5
            }

        return result
        
    def __stringIntDecimalToString(self, tripleList):
        resultString = ''
        for (string, integer, decimal) in tripleList:
             resultString += string + ',' + str(integer) + ',' + str(decimal) + ';'
        return resultString
    
    def __stringIntToString(self, pairList):
        resultString = ''
        for (string, integer) in pairList:
             resultString += string + ',' + str(integer) + ';'
        return resultString
    
    def __decisionListFromPkString(self, string):
        if not string:
            return []
        pkList = [int(x) for x in string.split(',')]
        result = []
        for pk in pkList:
            decision = DecisionModelProxy.GetDecisionFromPrimaryKey(pk)
            if decision:
                result.append(decision)
        return result

    def __pkValueToDecisionValue(self, pairs):
        result = []
        for (pk, value) in pairs:
            decision = DecisionModelProxy.GetDecisionFromPrimaryKey(pk)
            if decision:
                result.append((decision, value))
        return result

    def __stringIntDecimalFromString(self, string):
        if not string:
            return []
        resultList = []
        for triple in string.split(';'):
            if not triple:
                continue
            tripleList = triple.split(',')
            resultList.append((tripleList[0], int(tripleList[1]), Decimal(tripleList[2])))
        return resultList    

    def __stringIntFromString(self, string):
        if not string:
            return []
        resultList = []
        for pair in string.split(';'):
            if not pair:
                continue
            pairList = pair.split(',')
            resultList.append((pairList[0], int(pairList[1])))
        return resultList

