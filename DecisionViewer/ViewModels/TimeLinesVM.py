from datetime import date
from DecisionViewer.ViewModels.Base import VMBase
from Decisions.AnalysisStorers import BoardTimelineAnalysisToDB
from Decisions.DBProxy import DecisionModelProxy

class TimeLinesViewModel(VMBase):
        
    def __init__(self):
        super(TimeLinesViewModel, self).__init__()
        self.__getAllAnalyses_andEarliestAndLatestYears()            
        self.__assembleYearline_andTimelines()

        self.Context.update( {
            'years': self.__yearLine,
            'boardtls': sorted(self.__timelines.items())
            } )


    def __getAllAnalyses_andEarliestAndLatestYears(self):

        self.__boardList = DecisionModelProxy.GetBoardList()
        self.__boardanalyses = {}
        self.__timelines = {}
        self.__earliest = date.max.year
        self.__latest = date.min.year

        for board in self.__boardList:           
            timeline = BoardTimelineAnalysisToDB.GetBoardTimelineAnalysisFromDB(board)             
            self.__boardanalyses[board] = timeline
            self.__timelines[board] = []
            self.__earliest = min(min(timeline.YearlyDecisions), self.__earliest)
            self.__latest = max(max(timeline.YearlyDecisions), self.__latest)


    def __assembleYearline_andTimelines(self):
        self.__yearLine = []
        for year in range(self.__earliest, self.__latest + 1):
            self.__yearLine.append(year)
            for board in self.__boardList:
                self.__timelines[board].append(self.__boardanalyses[board].YearlyDecisions.get(year, ' '))
        
        self.__timelines.pop('')
