from DecisionViewer.ViewModels.Base import VMBase
from Decisions.Analysers.Coordinators import PersistentBoardAnalysisCoordinator

class  BoardViewModel(VMBase):
    
    __analyser = PersistentBoardAnalysisCoordinator()

    def __init__(self, board):
        super().__init__()

        analysis = self.__analyser.GetAnalysis(board)

        if analysis:
            self.Context.update(self.__fullContext(board, analysis))
        else:
            self.Context.update(self.__miniContext(board))
       

    def __fullContext(self, board, analysis):      
        return {
            'board' : analysis.Board,
            'count' : analysis.Count,
            'earliest': analysis.Early,
            'latest': analysis.Late,
            'ipc' : analysis.IpcTop5,
            'provisions': analysis.ArticleTop5,
            'citations': analysis.CitationTop5,
            'title': 'Board ' + board
            }


    def __miniContext(self, board):
        return {
            'title' : 'Board ' + board + ':  no information.',
            }




