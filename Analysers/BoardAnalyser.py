from datetime import datetime, timedelta

from app.DBProxy import DecisionModelProxy

from Analysers import AnalysisHelpers
from Analysers.BoardAnalysis import *

class BoardAnalyser(object):
    
    def __init__(self, cachetimelimit:timedelta = timedelta(days=1)):
        self.__cache = {}
        self.__cacheTimeLimit = cachetimelimit
        self.__workingBoard = ''

    def GetAnalysis(self, board):
        self.__workingBoard = board
        self.__removeOldFromCache()
        needToAnalyse = self.__needToAnalyse()
        if needToAnalyse:
            analysis = self.__analyseAndCacheBoard()
        else:
            analysis = self.__cache[self.__workingBoard]            
        return analysis

    @property
    def CachedBoardList(self):
        return [board for board in self.__cache]

    def __needToAnalyse(self):
        if not self.__boardIsCached():
            return True
        if not self.__cacheAge_ok():
            return True
        return False

    def __boardIsCached(self):
        return self.__workingBoard in self.__cache

    def __cacheAge_ok(self):
        cachedAnalysis = self.__cache.get(self.__workingBoard, OutdatedBoardAnalysis())
        cacheAge = cachedAnalysis.Age
        return cacheAge <= self.__cacheTimeLimit

    def __analyseAndCacheBoard(self):
        boardList = DecisionModelProxy.GetBoardList()
        if self.__workingBoard not in boardList:
            return NullBoardAnalysis()

        boardDecisions = DecisionModelProxy.GetAllForBoardOrderedByDecisionDate(self.__workingBoard)
        count = boardDecisions.count()
        early = boardDecisions[:5]
        if count >= 5:
            late = boardDecisions[count-5:]
        else:
            late = boardDecisions

        ipcTop5 = AnalysisHelpers.IpcMainFrequencyForBoard_TopN_withPercentage(self.__workingBoard, 5, count)
        articleTop5 = AnalysisHelpers.ArticleFrequencyForBoard_TopN_withPercentage(self.__workingBoard, 5, count)
        citationTop5 = AnalysisHelpers.ArticleFrequencyForBoard_TopN(self.__workingBoard, 5)

        analysis = BoardAnalysis(
            self.__workingBoard,
            count,
            list(early),
            list(late),
            list(ipcTop5),
            list(articleTop5),
            list(citationTop5)
            )

        self.__cache[self.__workingBoard] = analysis
        return analysis

    def __removeOldFromCache(self):
        self.__cache = { board: analysis 
                        for board, analysis 
                        in self.__cache.items() 
                        if analysis.Age < self.__cacheTimeLimit }



    

