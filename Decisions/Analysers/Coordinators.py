from Decisions.Analysers.BoardAnalyser import BoardAnalyser
from Decisions.Analysers.TimelineAnalysers import BoardTimelineAnalyser
from Decisions.AnalysisStorers import BoardAnalysisToDB
from Decisions.AnalysisStorers import BoardTimelineAnalysisToDB 

class PersistentBoardAnalysisCoordinator(object):

    def __init__(self):
        self.__analyser = BoardAnalyser()

    def GetAnalysis(self, board):
        boardIsCached = self.__analyser.BoardIsCached(board)
        if boardIsCached:
            analysis = self.__analyser.GetAnalysis(board)
        else:
            dbAnalysis = BoardAnalysisToDB.GetBoardAnalysisFromDB(board)
            if dbAnalysis.IsValid:
                analysis = dbAnalysis
            else:
                analysis = self.__analyser.GetAnalysis(board)
                BoardAnalysisToDB.SaveBoardAnalysisToDB(analysis)
        return analysis


class PersistentTimelineAnalysisCoordinator(object):
    
    def __init__(self):
        self.__boardAnalyser = BoardAnalyser()
        self.__timelineAnalyser = BoardTimelineAnalyser()

    def GetAnalysis(self, board):
        boardIsCached = self.__timelineAnalyser.BoardIsCached(board)
        if boardIsCached:
            timelineAnalysis = self.__timelineAnalyser.GetAnalysis(board)
            return timelineAnalysis

        dbBoardAnalysis = BoardAnalysisToDB.GetBoardAnalysisFromDB(board)
        if not dbBoardAnalysis.IsValid:
            boardAnalysis = self.__boardAnalyser.GetAnalysis(board)
            BoardAnalysisToDB.SaveBoardAnalysisToDB(boardAnalysis)

        dbTimelineAnalysis = BoardTimelineAnalysisToDB.GetBoardTimelineAnalysisFromDB(board)            
        if dbTimelineAnalysis.IsValid and dbTimelineAnalysis.YearlyDecisions:
            timelineAnalysis = dbTimelineAnalysis
        else:
            timelineAnalysis = self.__timelineAnalyser.GetAnalysis(board)
            BoardTimelineAnalysisToDB.SaveBoardTimelineAnalysisToDB(timelineAnalysis)

        return timelineAnalysis










