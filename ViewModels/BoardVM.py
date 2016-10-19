from ViewModels.Base import VMBase
#from Analysers.Persistent import PersistentAnalyser
from Analysers.BoardAnalyser import BoardAnalyser

class  BoardViewModel(VMBase):
    
    #__analyser = PersistentAnalyser()
    __analyser = BoardAnalyser()

    def __init__(self, board):
        super(BoardViewModel, self).__init__()

        #analysis = self.__analyser.GetBoardAnalysis(board)
        analysis = self.__analyser.GetAnalysis(board)

        if analysis:
            self.Context.update(self.__fullContext(board, analysis))
        else:
            self.Context.update(self.__miniContext(board))
       

    def __fullContext(self, board, analysis):
        #return {
        #    'board' : analysis['board'],
        #    'count' : analysis['count'],
        #    'earliest': analysis['early'],
        #    'latest': analysis['late'],
        #    'ipc' : analysis['ipctop'],
        #    'provisions': analysis['articletop'],
        #    'citations': analysis['citationtop'],
        #    'title': 'Board ' + board
        #    }        
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




