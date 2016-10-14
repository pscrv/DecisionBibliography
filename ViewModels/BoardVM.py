from app.DBAnalyser import BoardAnalyser
from app.DBAnalyser import PersistentAnalyser

class  BoardViewModel(object):
    
    __analyser = BoardAnalyser()

    def __init__(self, board):

        #analysis = self.__analyser.AnalyseBoard(board)

        #self.Context = {
        #    'board' : board,
        #    'count' : analysis['count'],
        #    'earliest': analysis['early'],
        #    'latest': analysis['late'],
        #    'ipc' : analysis['ipctop'],
        #    'provisions': analysis['articletop'],
        #    'citations': analysis['citationtop'],
        #    'title': 'Board ' + board
        #    }


        analyser = PersistentAnalyser()
        analysis = analyser.GetBoardAnalysis(board)
        self.Context = {
            'board' : board,
            'count' : analysis.Count,
            'earliest': analysis.Earliest,
            'latest': analysis.Latest,
            'ipc' : analysis.IPC_TopFive,
            'provisions': analysis.Article_TopFive,
            'citations': analysis.Cited_TopFive,
            'title': 'Board ' + board
            }




