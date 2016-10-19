import datetime
from app import DateHelpers

from Analysers.AnalysisBase import TimestampBase

class BoardTimelineAnalysis(TimestampBase):

    def __init__(self, board):
        self.Board = board
        self.YearlyDecisions = {}

    
    def MakeFromTimeline(self, timeline):
        self.YearlyDecisions = self.__accumulateMonthsToYears(timeline)

    ###
    #working here
    ###
    #must change this so that firstDate and lastDate can be extracted from timeline
    def __accumulateMonthsToYears(self, timeline):
        yearlyDecisions = {}
        from app.DBProxy import DecisionModelProxy
        decisions = DecisionModelProxy.GetAllForBoardOrderedByDecisionDate(self.Board)
        firstDate = decisions.first().DecisionDate
        lastDate = decisions.last().DecisionDate
        for year in DateHelpers.YearIterator(firstDate, lastDate):
            count = 0
            for month in DateHelpers.MonthIteratorOneYear(year):
                count += timeline.get(month, 0)
            yearlyDecisions[year] = count
        return yearlyDecisions