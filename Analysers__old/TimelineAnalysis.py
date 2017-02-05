from app.DBProxy import DecisionModelProxy

from Analysers.AnalysisBase import TimestampBase
class BoardTimelineAnalysis(TimestampBase):

    def __init__(self, board, yearlydecisions = {}):
        super(BoardTimelineAnalysis, self).__init__()
        self.Board = board
        self.YearlyDecisions = yearlydecisions




    
class NullBoardTimelineAnalysis(BoardTimelineAnalysis):

    def __init__(self):
        super(NullBoardTimelineAnalysis, self).__init__(board = 'Nosuchboard')


    def __eq__(self, other):
        if isinstance(other, NullBoardTimelineAnalysis):
            return True
        return False

    @property
    def IsValid(self):
        return False



        
class EmptyBoardTimelineAnalysis(BoardTimelineAnalysis):

    def __init__(self, board):
        super(EmptyBoardTimelineAnalysis, self).__init__(board = board)
        
    def __eq__(self, other):
        if isinstance(other, EmptyBoardTimelineAnalysis) and other.Board == self.Board:
            return True
        return False
