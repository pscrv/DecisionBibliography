from datetime import datetime
from Analysers.AnalysisBase import TimestampBase

class BoardAnalysis(TimestampBase):

    def __init__(self, board = '', count = 0, early = [], late = [], ipcTop5 = [], articleTop5 = [], citationTop5 = []):
        super(BoardAnalysis, self).__init__()

        self.Board = board
        self.Count = count
        self.Early = early
        self.Late = late
        self.IpcTop5 = ipcTop5
        self.ArticleTop5 = articleTop5
        self.CitationTop5 = citationTop5
   
    
class NullBoardAnalysis(BoardAnalysis):

    def __init__(self):
        super(NullBoardAnalysis, self).__init__(board = 'Nosuchboard')
        
    def __eq__(self, other):
        if isinstance(other, NullBoardAnalysis):
            return True
        return False




