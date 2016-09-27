from app.DBAnalyser import BoardAnalyser

class  BoardViewModel(object):
    
    __analyser = BoardAnalyser()

    def __init__(self, bd):

        analysis = self.__analyser.AnalyseBoard(bd)

        self.Context = {
            'board' : bd,
            'count' : analysis['count'],
            'earliest': analysis['early'],
            'latest': analysis['late'],
            'ipc' : analysis['ipctop'],
            'provisions': analysis['articletop'],
            'citations': analysis['citationtop'],
            'title': 'Board ' + bd
            }




