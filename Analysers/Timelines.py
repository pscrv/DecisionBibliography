import datetime
from app import DateHelpers
from app.DBProxy import DecisionModelProxy


class TimelineAnylser(object):

    def __init__(self):
        self.__count = 0
        self.__boards = sorted(DecisionModelProxy.GetBoardList())
        self.__timelines = {}
        self.__earliestdate = None
        self.__latestdate = None
        self.__analysed = False
            
    def __analysePublishedDecisionTimelines(self):
        if self.__analysed:
            return

        orderedObjects = DecisionModelProxy.GetAllOrderedByDecisionDate()
        startDate = orderedObjects.first().DecisionDate
        endDate = orderedObjects.last().DecisionDate

        # get all boards and their timelines
        boards = []
        timelines = {}
        count = 0
        for dt in DateHelpers.MonthIterator(startDate, endDate):
            cases = DecisionModelProxy.GetAllInDateRange(dt, DateHelpers.EndOfThisMonth(dt))
                                
            for case in cases:
                bd = case.Board
                if not bd in boards:
                    boards.append(bd)
                    timelines[bd] = {}
                if not dt in timelines[bd]:
                    timelines[bd][dt] = 1
                else:
                    timelines[bd][dt] += 1
                count += 1

        self.__count = count
        self.__boards = sorted(boards)
        self.__timelines = timelines
        self.__earliestdate = startDate
        self.__latestdate = endDate
        self.__analysed = True
        
    def GetBoardTimeline(self, board):
        if board not in self.__boards:
            return None
        self.__analysePublishedDecisionTimelines()
        analysis =  BoardTimelineAnalysis(board)
        analysis.MakeFromTimeline(self.__timelines[board])
        return analysis

    def GetBoardList(self):
        return self.__boards

    def GetEarliestDate(self):
        self.__analysePublishedDecisionTimelines()
        return self.__earliestdate

    def GetLatestDate(self):
        self.__analysePublishedDecisionTimelines()
        return self.__latestdate

    def GetTotalCount(self):
        self.__analysePublishedDecisionTimelines()
        return self.__count

    

    def GetBoardTimelineAsString(self, board):
        self.__analysePublishedDecisionTimelines()
        timeline = self.GetBoardTimeline(board)
        result = self.__timelineAsString(timeline)
        return result

    def __timelineAsString(self, timeline):
        timelineString = ''
        for date, count in timeline.YearlyDecisions.items():
            dateString = date.strftime('%Y/%m/%d')
            countString = str(count)
            timelineString += dateString + '::' + countString + ';'
        return timelineString    

    def GetBoardTimelineFromString(self, string):
        timeline = {}
        for pair in string.split(';'):
            if not pair:
                continue
            pairList = pair.split('::')
            dateString = pairList[0]
            count = pairList[1]
            date = datetime.datetime.strptime(dateString, "%Y/%m/%d").date()
            timeline[date] = int(count)
        return timeline



class BoardTimelineAnalysis(object):

    def __init__(self, board):
        self.Board = board
        self.YearlyDecisions = None

    def MakeFromTimeline(self, timeline):
        self.YearlyDecisions = self.__accumulateTimelineYears(timeline)

    def __accumulateTimelineYears(self, timeline):
        yearlyDecisions = {}
        decisions = DecisionModelProxy.GetAllForBoardOrderedByDecisionDate(self.Board)
        firstDate = decisions.first().DecisionDate
        lastDate = decisions.last().DecisionDate
        for year in DateHelpers.YearIterator(firstDate, lastDate):
            count = 0
            for month in DateHelpers.MonthIteratorOneYear(year):
                count += timeline.get(month, 0)
            yearlyDecisions[year] = count
        return yearlyDecisions


