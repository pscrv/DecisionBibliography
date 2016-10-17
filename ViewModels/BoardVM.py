from ViewModels.Base import VMBase
from Analysers.Persistent import PersistentAnalyser

class  BoardViewModel(VMBase):
    
    __analyser = PersistentAnalyser()

    def __init__(self, board):
        super(BoardViewModel, self).__init__()

        analysis = self.__analyser.GetBoardAnalysis(board)

        if analysis:
            self.Context.update(self.__fullContext(board, analysis))
        else:
            self.Context.update(self.__miniContext(board))
       

    def __fullContext(self, board, analysis):
        return {
            'board' : analysis['board'],
            'count' : analysis['count'],
            'earliest': analysis['early'],
            'latest': analysis['late'],
            'ipc' : analysis['ipctop'],
            'provisions': analysis['articletop'],
            'citations': analysis['citationtop'],
            'title': 'Board ' + board
            }


    def __miniContext(self, board):
        return {
            'title' : 'Board ' + board + ':  no information.',
            }




