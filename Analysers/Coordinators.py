from Analysers.BoardAnalyser import BoardAnalyser
from Analysers.TimelineAnalysers import BoardTimelineAnalyser
from AnalysisStorers.BoardAnalysisToDB import GetBoardAnalysisFromDB
from AnalysisStorers.BoardTimelineAnalysisToDB import GetBoardTimelineAnalysisFromDB

class PersistentBoardAnalysisCoordinator(object):

    def __init__(self):
        self.__analyser = BoardAnalyser()

    def GetAnalysis(self, board):
        boardIsCached = self.__analyser.BoardIsCached(board)
        if boardIsCached:
            analysis = self.__analyser.GetAnalysis(board)
        else:
            dbAnalysis = GetBoardAnalysisFromDB(board)
            found = dbAnalysis.IsValid
            if found:
                analysis = dbAnalysis
            else:
                analysis = self.__analyser.GetAnalysis(board)
        return analysis


class PersistentTimelineAnalysisCoordinator(object):
    
    def __init__(self):
        self.__analyser = BoardTimelineAnalyser()

    def GetAnalysis(self, board):
        boardIsCached = self.__analyser.BoardIsCached(board)
        if boardIsCached:
            analysis = self.__analyser.GetAnalysis(board)
        else:
            dbAnalysis = GetBoardTimelineAnalysisFromDB(board)
            found = dbAnalysis.IsValid
            if found:
                analysis = dbAnalysis
            else:
                analysis = self.__analyser.GetAnalysis(board)
        return analysis










