from django.core.management.base import BaseCommand

from Decisions.models import DecisionBibliographyModel
from Decisions.Analysers.BoardAnalyser import BoardAnalyser
from Decisions.Analysers.TimelineAnalysers import BoardTimelineAnalyser
from Decisions.AnalysisStorers import BoardAnalysisToDB, BoardTimelineAnalysisToDB

class Command(BaseCommand):
    help = 'Analyses the DB to extract information on individual boards. Results are stored in Decisions.models.BoardAnalysisModel'
    # See https://docs.djangoproject.com/en/1.9/howto/custom-management-commands/#module-django.core.management

    
    def handle(self, *args, **options):
        
        boardlist = [
            '3.1.01',
            '3.2.01', '3.2.02', '3.2.03', '3.2.04', '3.2.05', '3.2.06', '3.2.07', '3.2.08',
            '3.3.01', '3.3.02', '3.3.03', '3.3.04', '3.3.05', '3.3.06', '3.3.07', '3.3.08', '3.3.09', '3.3.10', 
            '3.4.01', '3.4.02', '3.4.03', 
            '3.5.01', '3.5.02', '3.5.03', '3.5.04', '3.5.05', '3.5.06', '3.5.07',
            'EBA',
            'DBA',
            ]

        for board in boardlist:
            self._analyseAndSave(board)



    def _analyseAndSave(self, board):
        self.stdout.write('Analysing {}.'.format(board))
        boardAnalyser = BoardAnalyser()        
        boardAnalysis = boardAnalyser.GetAnalysis(board)
        BoardAnalysisToDB.SaveBoardAnalysisToDB(boardAnalysis)

        timelineAnalyser = BoardTimelineAnalyser()
        timelineAnalysis = timelineAnalyser.GetAnalysis(board)
        BoardTimelineAnalysisToDB.SaveBoardTimelineAnalysisToDB(timelineAnalysis)








