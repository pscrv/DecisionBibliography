from app.DBAnalyser import BoardAnalyser
from app.DBAnalyser import PersistentAnalyser

class  BoardViewModel(object):
    
    #__analyser = BoardAnalyser()
    __analyser = PersistentAnalyser()

    def __init__(self, board):

        analysis = self.__analyser.GetBoardAnalysis(board)

        if analysis:
            self.Context = {
                'board' : analysis['board'],
                'count' : analysis['count'],
                'earliest': analysis['early'],
                'latest': analysis['late'],
                'ipc' : analysis['ipctop'],
                'provisions': analysis['articletop'],
                'citations': analysis['citationtop'],
                'title': 'Board ' + board
                }
        else:
            self.Context = {
                'title' : 'Board ' + board + ':  no information.',
                }
            




