from Analysers.BoardAnalyser import BoardAnalyser
from AnalysisStorers.BoardAnalysisToDB import GetBoardAnalysisFromDB

class PersistentAnalysisCoordinator(object):

    def __init__(self):
        self.__analyser = BoardAnalyser()

    def GetAnalysis(self, board):
        boardIsCached = self.__analyser.BoardIsCached(board)
        if boardIsCached:
            analysis = self.__analyser.GetAnalysis(board)
        else:
            dbAnalysis = GetBoardAnalysisFromDB(board)
            notFound = dbAnalysis.Board == 'Nosuchboard'
            if notFound:
                analysis = self.__analyser.GetAnalysis(board)
            else:
                analysis = dbAnalysis
        return analysis
