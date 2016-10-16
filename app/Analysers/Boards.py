import re
from decimal import Decimal
from app.DBProxy import DecisionModelProxy
from app.Analysers.AnalysisHelpers import IpcFrequencyForBoard, ArticleFrequencyForBoard, CitationFrequencyForBoard


class BoardAnalyser(object):

    def __init__(self):
        self.__cache = {}


    def GetBoardAnalysis(self, board):
        if board in self.__cache:
            return self.__cache[board]

        analysis = self.__analyseBoard(board)
        self.__cache[board] = analysis
        return analysis


    def __analyseBoard(self, board):
        
        boardDecisions = DecisionModelProxy.GetAllForBoardOrderedByDecisionDate(board)
        count = boardDecisions.count()
        early = boardDecisions[:5]
        if count >= 5:
            late = boardDecisions[count-5:]
        else:
            late = boardDecisions

        ipcFrequencies = IpcFrequencyForBoard(board)
        ipcMainFrequencies = self.__ipcToIpcMain(ipcFrequencies)
        ipcTop5 = self.__topNFromDictionaryWithPercentage(ipcMainFrequencies, 5, count)

        articleFrequencies = ArticleFrequencyForBoard(board)
        articleTop5 = self.__topNFromDictionaryWithPercentage(articleFrequencies, 5, count)

        citationFrequencies = CitationFrequencyForBoard(board)
        citationTop5 = self.__topNFromDictionary(citationFrequencies, 5)

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


    def __ipcToIpcMain(self, ipcdict):
        mainFrequencies = {}
        finder = re.compile(r'(.*)/(.*)')
        for cl in ipcdict:
            found = re.search(finder, cl)
            if not found:
                continue
            main = found.group(1)
            mainFrequencies[main] = mainFrequencies.get(main, 0) + ipcdict[cl]
        return mainFrequencies
    
    def __topNFromDictionaryWithPercentage(self, dict, n, total):
        keyList = sorted(dict.keys(), key=(lambda k: dict[k]), reverse = True)[:n]
        return [ (k, dict[k], round(Decimal(100 * dict[k] / total), 2)) for k in keyList]

    def __topNFromDictionary(self, dict, n):    
        keyList = sorted(dict.keys(), key=(lambda k: dict[k]), reverse = True)[:n]
        return [ (k, dict[k]) for k in keyList]

    def __appendPercentage (self, pairList, total):
        return [ (x, y, round(Decimal(100 *y / total), 2)) for (x, y) in pairList]


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

