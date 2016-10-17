import datetime

from app import DateHelpers
from app.DBProxy import DecisionModelProxy
from app.models import BoardAnalysisModel
from Analysers.Timelines import TimelineAnylser
from Analysers.Boards import BoardAnalyser


class PersistentAnalyser(object):

    def __init__(self):
        self.__boardList = DecisionModelProxy.GetBoardList()
        self.__boardAnalyser = BoardAnalyser()
        self.__timelineAnalyser = TimelineAnylser()
        self.__boardAnalyses = {}


    def AnalyseBoard(self, board):
        self.__analyseAndStoreOneBoard(board)


    def GetBoardAnalysis(self, board):
        if not board in self.__boardList:
            return {}

        recoveredAnalysis, created = BoardAnalysisModel.objects.get_or_create(Board = board)
        if created:
            analysis = self.__analyseAndStoreOneBoard(board)
        else:
            savableAnalysis = self.__recoveredAnalysisToSavableBoardAnalysis(recoveredAnalysis)
            analysis = self.__boardAnalyser.ParseSavableBoardAnalysis(savableAnalysis)
        return analysis

    def __analyseAndStoreOneBoard(self, board):
        #self.__setAnalysersIfNeeded()
        self.__boardAnalyses[board] = self.__boardAnalyser.GetBoardAnalysis(board)        
        self.__storeOneBoard(board)
        return self.__boardAnalyses[board]

    def __setAnalysersIfNeeded(self):
        if not self.__timelineAnalyser:
            self.__timelineAnalyser = TimelineAnylser()
        if not self.__boardAnalyser:
            self.__boardAnalyser = BoardAnalyser()

    def __recoveredAnalysisToSavableBoardAnalysis(self, recoveredAnalysis):
        savableBoardAnalysis = {
            'board': recoveredAnalysis.Board,
            'count': recoveredAnalysis.Count,
            'early': recoveredAnalysis.EarliestFive,
            'late': recoveredAnalysis.LatestFive,
            'ipctop': recoveredAnalysis.IPC_TopFive,
            'articletop': recoveredAnalysis.Article_TopFive,
            'citationtop': recoveredAnalysis.Cited_TopFive,
            }

        return savableBoardAnalysis

    def __storeOneBoard(self, board):
        savableTimeline = self.__timelineAnalyser.GetBoardTimelineAsString(board)
        savableBoardAnalysis = self.__boardAnalyser.GetSavableBoardAnalysis(board)

        persistentAnalysis, created = BoardAnalysisModel.objects.get_or_create(Board = board)
        persistentAnalysis.Count = savableBoardAnalysis['count']
        persistentAnalysis.EarliestFive = savableBoardAnalysis['early']
        persistentAnalysis.LatestFive = savableBoardAnalysis['late']
        persistentAnalysis.IPC_TopFive = savableBoardAnalysis['ipctop']
        persistentAnalysis.Article_TopFive = savableBoardAnalysis['articletop']
        persistentAnalysis.Cited_TopFive = savableBoardAnalysis['citationtop']  
        persistentAnalysis.Timeline = savableTimeline
        persistentAnalysis.save()

    def __getOneBoardStoredAnalysis(self, board):
        gotAnalysis, created = BoardAnalysisModel.objects.get_or_create(Board = board)
        if created:
            return None
        
        boardAnalysis = {
            'count' : gotAnalysis.Count,
            'ipctop' : gotAnalysis.IPC_TopFive,
            'articletop' : gotAnalysis.Article_TopFive,
            'citationtop' : gotAnalysis.Cited_TopFive,
            }
        yearlyCount = self.__timelineFromString(gotAnalysis.YearlyCount)  
        
    def __timelineAsString(self, timeline):
        timelineString = ''
        for date, count in timeline.YearlyDecisions.items():
            dateString = date.strftime('%Y/%m/%d')
            countString = str(count)
            timelineString += dateString + '::' + countString + ';'
        return timelineString
    
    def __timelineFromString(self, string):
        timeline = {}
        for pair in string.split(';'):
            if not pair:
                continue
            pairList = pair.split('::')
            dateString = pairList[0]
            count = pairList[1]
            date = datetime.datetime.strptime(dateString, "%Y/%m/%d").date()
            timeline[date] = int(count)
        return timeline
    

    def GetAllBoardTimelines(self):
        #self.__setAnalysersIfNeeded()

        boardanalyses = {}
        tls = {}
        earliest = datetime.date.max
        latest = datetime.date.min
        for board in self.__boardList:

            #working here
            recoveredAnalysis, created = BoardAnalysisModel.objects.get_or_create(Board = board)
            if created:
                self.__analyseAndStoreOneBoard(board)
                recoveredAnalysis, create = BoardAnalysisModel.objects.get_or_create(Board = board)
                
            timeline = self.__timelineAnalyser.GetBoardTimelineFromString(recoveredAnalysis.Timeline)            
            boardanalyses[board] = timeline
            tls[board] = []
            early = min(timeline)
            earliest = min(early, earliest)
            late = max(timeline)
            latest = max(late, latest)

        tls['years'] = []
        for year in DateHelpers.YearIterator(earliest, latest):
            tls['years'].append(year)
            for board in self.__boardList:
                tls[board].append(boardanalyses[board].get(year, ' '))
        return tls          

