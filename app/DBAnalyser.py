import datetime
import re
from decimal import Decimal
from . models import DecisionBibliographyModel as DB
from . import DateHelpers


class Analyser(object):
    def GetAttributeFrequency(self, attribute, decisions):
        if not attribute in vars(DB):
            return None
        result = {}
        for decision in decisions:
            value = decision.__dict__[attribute]
            if DB.objects.IsListAttribute(attribute):
                values = [x.strip() for x in value.split(',')]
            else:
                values = [value.strip()]
            for v in values:
                result[v] = result.get(v, 0) + 1
        return result



class PublishedDecisionTimelineAnalyser(Analyser):
    """description of class"""
    
    def AnalysePublishedDecisionTimelines(self):
        if self.__analysed:
            return

        self.ObjectCount = self.__dbobjects.count()
        orderedObjects = self.__dbobjects.order_by('DecisionDate')
        startDate = orderedObjects.first().DecisionDate
        endDate = orderedObjects.last().DecisionDate

        # get all boards and their timelines
        boards = []
        timelines = {}
        count = 0
        for dt in DateHelpers.MonthIterator(startDate, endDate):
            cases = self.__dbobjects.FilterOnlyPrLanguage(DecisionDate__range = (dt, DateHelpers.EndOfThisMonth(dt)))
                                
            for case in cases:
                bd = case.Board
                if not bd in boards:
                    boards.append(bd)
                    timelines[bd] = {}
                if not dt in timelines[bd]:
                    timelines[bd][dt] = 1
                else:
                    timelines[bd][dt] += 1
                count += 1

        self.__count = count
        self.__boards = sorted(boards)
        self.__timelines = timelines
        self.__earliestdate = startDate
        self.__latestdate = endDate
        self.__analysed = True

    def AnalyseBoardPublishedDecisionTimeline(self, board):
        if not self.__analysed:
            self.AnalysePublishedDecisionTimelines()
        if board not in self.__boards:
            return None
        return BoardTimelineAnalysis(board, self. __timelines[board])

    def AnalyseAllBoardsPublishedDecisionTimeline(self):
        boarddanalyses = []
        for board in self.__boards:
            analysis = self.AnalyseBoardPublishedDecisionTimeline(board)
            boarddanalyses.append(analysis)
        return boarddanalyses

    def GetBoardTimeline(self, board):
        analysis = self.AnalyseBoardPublishedDecisionTimeline(board)
        if analysis == None: 
            return None
        start = analysis.FirstDecisionDate
        end = analysis.LatestDecisionDate
        yearlist = []
        timeline = []
        for year in DateHelpers.YearIterator(start, end):
            yearlist.append(year)
            timeline.append(analysis.YearlyDecisions.get(year, ' '))
        return { 'years': yearlist, 'amount': timeline }

    def GetAllBoardTimelines(self):
        boardanalyses = {}
        tls = {}
        for board in self.__boards:
            boardanalyses[board] = self.AnalyseBoardPublishedDecisionTimeline(board)
            tls[board] = []
        tls['years'] = []

        for year in DateHelpers.YearIterator(self.__earliestdate, self.__latestdate):
            tls['years'].append(year)
            for board in self.__boards:
                tls[board].append(boardanalyses[board].YearlyDecisions.get(year, ' '))
        return tls


    def __init__(self):
        self.__dbobjects = DB.objects
        self.__count = 0
        self.__boards = []
        self.__timelines = {}
        self.__analysed = False
        self.__earliestdate = None
        self.__latestdate = None



class BoardAnalyser(Analyser):

    def AnalyseBoard(self, board):
        if board in self.cache:
            return self.cache[board]
        
        boardDecisions =  DB.objects.FilterOnlyPrLanguage(Board = board).order_by('DecisionDate')
        count = boardDecisions.count()
        early = boardDecisions[:5]
        if count >= 5:
            late = boardDecisions[count-5:]
        else:
            late = boardDecisions

        ipcAnalyser = IPCAnalyser()
        ipcFrequencies = ipcAnalyser.IpcFrequencyForBoard(board)
        ipcMainFrequencies = self.__ipcToIpcMain(ipcFrequencies)
        ipcTop5 = self.__topNFromDictionaryWithPercentage(ipcMainFrequencies, 5, count)

        provisionAnalyser = ProvisionAnalyser()
        articleFrequencies = provisionAnalyser.ArticleFrequencyForBoard(board)
        articleTop5 = self.__topNFromDictionaryWithPercentage(articleFrequencies, 5, count)

        citationAnalyser = CitationAnalyser()
        citationFrequencies = citationAnalyser.CitationFrequencyForBoard(board)
        citationTop5 = self.__topNFromDictionary(citationFrequencies, 5)

        self.cache[board] =  {
            'count': count, 
            'early': early, 
            'late': late, 
            'ipctop': ipcTop5, 
            'articletop': articleTop5, 
            'citationtop': citationTop5
            }
        return self.cache[board]

    def __ipcToIpcMain(self, ipcdict):
        mainFrequencies = {}
        finder = re.compile(r'(.*)/(.*)')
        for cl in ipcdict:
            found = re.search(finder, cl)
            if not found:
                continue
            main = found.group(1)
            mainFrequencies[main] = mainFrequencies.get(main, 0) + ipcdict[cl]
        return mainFrequencies
    
    def __topNFromDictionaryWithPercentage(self, dict, n, total):
        keyList = sorted(dict.keys(), key=(lambda k: dict[k]), reverse = True)[:n]
        return [ (k, dict[k], round(Decimal(100 * dict[k] / total), 2)) for k in keyList]

    def __topNFromDictionary(self, dict, n):    
        keyList = sorted(dict.keys(), key=(lambda k: dict[k]), reverse = True)[:n]
        return [ (k, dict[k]) for k in keyList]

    def __appendPercentage (self, pairList, total):
        return [ (x, y, round(Decimal(100 *y / total), 2)) for (x, y) in pairList]


    def __init__(self):
        self.cache = {}


class IPCAnalyser(Analyser):

    def IpcFrequency(self, decisions):
        return self.GetAttributeFrequency('IPC', decisions)

    def IpcFrequencyForBoard(self, board):
        decisions = DB.objects.FilterOnlyPrLanguage(Board = board)
        return self.IpcFrequency(decisions)
        

class ProvisionAnalyser(Analyser):

    def ArticleFrequency(self, decisions):
        return self.GetAttributeFrequency('Articles', decisions)

    def ArticleFrequencyForBoard(self, board):
        decisions = DB.objects.FilterOnlyPrLanguage(Board = board)
        return self.ArticleFrequency(decisions)
    
    def RuleFrequency(self, decisions):
        return self.GetAttributeFrequency('Rules', decisions)

    def RuleFrequencyForBoard(self, board):
        decisions = DB.objects.FilterOnlyPrLanguage(Board = board)
        return self.RuleFrequency(decisions)


class CitationAnalyser(Analyser):
    
    def CitationFrequency(self, decisions):
        result = {}
        for decision in decisions:
            result[decision] = DB.objects.FilterOnlyPrLanguage(CitedCases__contains = decision.CaseNumber).count()
        return result

    def CitationFrequencyForBoard(self, board):
        decisions = DB.objects.FilterOnlyPrLanguage(Board = board)
        return self.CitationFrequency(decisions)



class BoardTimelineAnalysis(object):

    def __init__(self, board, timeline):
        self.Board = board
        self.Timeline = timeline
        self.FirstDecisionCaseNumber, self.FirstDecisionDate = self.__getEarliestDecisionOfMonth(min(self.Timeline))
        self.LatestDecisionCaseNumber, self.LatestDecisionDate = self.__getLastestDecisionOfMonth(max(self.Timeline))
        self.YearlyDecisions = {}

        for year in DateHelpers.YearIterator(self.FirstDecisionDate, self.LatestDecisionDate):
            count = 0
            for month in DateHelpers.MonthIteratorOneYear(year):
                count += self.Timeline.get(month, 0)
            self.YearlyDecisions[year] = count


    def __getEarliestDecisionOfMonth(self, dt:datetime):
        return self.__getFirstOfMonth(dt)

    def __getLastestDecisionOfMonth(self, dt:datetime):
        return self.__getFirstOfMonth(dt, descending=True)

    def __getFirstOfMonth(self, dt:datetime, descending=False):
        sorter = 'DecisionDate'
        if descending: 
            sorter = '-DecisionDate'
        decisions = DB.objects.FilterOnlyPrLanguage(
           Board = self.Board,
           DecisionDate__range = (
              DateHelpers.FirstOfThisMonth(dt), 
              DateHelpers.EndOfThisMonth(dt))).order_by(sorter)
        return decisions.first().CaseNumber, decisions.first().DecisionDate





