from datetime import datetime, timedelta

from Decisions.DBProxy import DecisionModelProxy

from Decisions.Analysers import AnalysisHelpers
from Decisions.Analysers.BoardAnalysis import BoardAnalysis, NullBoardAnalysis
from Decisions.Analysers.AnalyserBase import CachingBase

class BoardAnalyser(CachingBase):
    
    def __init__(self, cachetimelimit: timedelta = timedelta(days=1)):
        super(BoardAnalyser, self).__init__(cachetimelimit)


    @property
    def CachedBoardList(self):
        return self._cachedKeyList()

    def BoardIsCached(self, board):
        return board in self.CachedBoardList
    

    def _analyseAndCache(self, board):
        boardList = DecisionModelProxy.GetBoardList()
        if board not in boardList:
            return NullBoardAnalysis()

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

        analysis = BoardAnalysis(
            board,
            count,
            list(early),
            list(late),
            list(ipcTop5),
            list(articleTop5),
            list(citationTop5)
            )

        self._cache[board] = analysis
        return analysis

   


    

