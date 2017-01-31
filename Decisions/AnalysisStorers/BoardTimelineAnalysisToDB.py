from datetime import datetime
from Decisions.models import BoardAnalysisModel
from Decisions.DBProxy import DecisionModelProxy

from Decisions.Analysers.TimelineAnalysis import *


def SaveBoardTimelineAnalysisToDB(analysis):
   
    dbAnalysis, created = BoardAnalysisModel.objects.get_or_create(Board = analysis.Board)
    dbAnalysis.Timeline = _yearlyDecisionsToString(analysis.YearlyDecisions)
    dbAnalysis.save()


def GetBoardTimelineAnalysisFromDB(board):

    dbAnalysis = BoardAnalysisModel.objects.filter(Board = board).first()
    if dbAnalysis is None:
        return NullBoardTimelineAnalysis()
    if not dbAnalysis.Timeline:
        return EmptyBoardTimelineAnalysis(board)    

    timelineAnalysis = BoardTimelineAnalysis(
        board,
        _yearlyDecisionsFromString(dbAnalysis.Timeline)
        )

    return timelineAnalysis



def _yearlyDecisionsToString(timeline):
    timelineString = ''
    for year, count in timeline.items():
        yearString = str(year)
        countString = str(count)
        timelineString += yearString + '::' + countString + ';'
    return timelineString    


def _yearlyDecisionsFromString(string):

    timeline = {}
    for pair in string.split(';'):
        if not pair:
            continue
        pairList = pair.split('::')
        year = int(pairList[0])
        count = int(pairList[1])
        timeline[year] = int(count)
    return timeline
