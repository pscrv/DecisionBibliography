from datetime import datetime, timedelta

from Decisions import DateHelpers
#from Decisions.DBProxy import DecisionModelProxy
from DecisionsPlus import DecisionModelProxy
from Decisions.Analysers.TimelineAnalysis import *
from Decisions.Analysers.AnalyserBase import CachingBase

class BoardTimelineAnalyser(CachingBase):

    def __init__(self, cachetimelimit: timedelta = timedelta(days=1)):
        super(BoardTimelineAnalyser, self).__init__(cachetimelimit)
                

    @property
    def CachedBoardList(self):
        return self._cachedKeyList()
    
    def BoardIsCached(self, board):
        return board in self.CachedBoardList
        
    def _analyseAndCache(self, board):
        boardList = DecisionModelProxy.GetBoardList()
        if board not in boardList:
            return NullBoardTimelineAnalysis()
        
        boardDecisions = DecisionModelProxy.GetAllForBoardOrderedByDecisionDate(board)
        if not boardDecisions:
            return EmptyBoardTimelineAnalysis(board)

        earliestDate = boardDecisions[0].DecisionDate
        latestDate = boardDecisions[-1].DecisionDate

        yearlyCases = {}
        for year in DateHelpers.YearIterator(earliestDate, latestDate):
            yearDecisions = [x for x in boardDecisions if x.DecisionDate.year == year.year]
            yearCount = len(yearDecisions)
            yearlyCases[year.year] = yearCount            
        result = BoardTimelineAnalysis(board, yearlyCases)
        self._cache[board] = result
        return result


    
