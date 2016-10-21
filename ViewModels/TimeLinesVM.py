from datetime import date
from ViewModels.Base import VMBase
#from Analysers.Persistent import PersistentAnalyser
from Analysers.Coordinators import PersistentTimelineAnalysisCoordinator
from app.DBProxy import DecisionModelProxy

class TimeLinesViewModel(VMBase):
        
    #__analyser = PersistentAnalyser()
    __analyser = PersistentTimelineAnalysisCoordinator()

    def __init__(self):
        super(TimeLinesViewModel, self).__init__()

        boardList = DecisionModelProxy.GetBoardList()
        boardanalyses = {}
        timelines = {}
        earliest = date.max.year
        latest = date.min.year
        for board in boardList:           
            timeline = self.__analyser.GetAnalysis(board)            
            boardanalyses[board] = timeline
            timelines[board] = []
            earliest = min(min(timeline.YearlyDecisions), earliest)
            latest = max(max(timeline.YearlyDecisions), latest)

        timelines['years'] = []
        for year in range(earliest, latest + 1):
            timelines['years'].append(year)
            for board in boardList:
                timelines[board].append(boardanalyses[board].YearlyDecisions.get(year, ' '))
             


        yearline = timelines['years']
        timelines.pop('')
        timelines.pop('years')    

        self.Context.update( {
            'years': yearline, 
            'boardtls': sorted(timelines.items())
            } )
