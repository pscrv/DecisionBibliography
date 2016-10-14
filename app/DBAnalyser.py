import datetime
import re
from decimal import Decimal
from app.DBProxy import DecisionModelProxy
from app.models import BoardAnalysisModel
from app import DateHelpers


class Analyser(object):
    def GetAttributeFrequency(self, attribute, decisions):
        if not attribute in DecisionModelProxy.GetBibliographyAttributeList():
            return None
        result = {}
        for decision in decisions:
            value = decision.__dict__[attribute]
            if DecisionModelProxy.GetIsListAttribute(attribute):
                values = [x.strip() for x in value.split(',')]
            else:
                values = [value.strip()]
            for v in values:
                result[v] = result.get(v, 0) + 1
        return result


class PersistentAnalyser(Analyser):

    def __init__(self):
        self.__boardList = DecisionModelProxy.GetBoardList()
        self.__boardAnalyser = None
        self.__timelineAnalyser = None
        self.__boardAnalyses = {}


    def AnalyseBoard(self, board):
        self.__analyseAndStoreOneBoard(board)


    def GetBoardAnalysis(self, board):
        if not board in self.__boardList:
            return None

        # delete this soon
        #for board in self.__boardList:
        #    self.__analyseAndStoreOneBoard(board)
        self.__analyseAndStoreOneBoard(board)

        recoveredAnalysis, created = BoardAnalysisModel.objects.get_or_create(Board = board)
        if created:
            analysis = self.__analyseAndStoreOneBoard(board)
        else:
            savableAnalysis = self.__recoveredAnalysisToSavableBoardAnalysis(recoveredAnalysis)
            analysis = self.__boardAnalyser.ParseSavableBoardAnalysis(savableAnalysis)
        return analysis


    def __analyseAndStoreOneBoard(self, board):
        self.__setAnalysersIfNeeded()
        self.__boardAnalyses[board] = self.__boardAnalyser.GetBoardAnalysis(board)        
        self.__storeOneBoard(board)

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


            



class TimelineAnylser(Analyser):

    def __init__(self):
        self.__count = 0
        self.__boards = []
        self.__timelines = {}
        self.__earliestdate = None
        self.__latestdate = None
        self.__analysed = False
        self.AnalysePublishedDecisionTimelines()
            
    def AnalysePublishedDecisionTimelines(self):
        if self.__analysed:
            return

        orderedObjects = DecisionModelProxy.GetAllOrderedByDecisionDate()
        startDate = orderedObjects.first().DecisionDate
        endDate = orderedObjects.last().DecisionDate

        # get all boards and their timelines
        boards = []
        timelines = {}
        count = 0
        for dt in DateHelpers.MonthIterator(startDate, endDate):
            cases = DecisionModelProxy.GetAllInDateRange(dt, DateHelpers.EndOfThisMonth(dt))
                                
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

        
    def GetBoardTimeline(self, board):
        if board not in self.__boards:
            return None
        analysis =  BoardTimelineAnalysis(board)
        analysis.MakeFromTimeline(self.__timelines[board])
        return analysis

    def GetBoardList(self):
        return self.__boards

    def GetEarliestDate(self):
        return self.__earliestdate

    def GetLatestDate(self):
        return self.__latestdate

    def GetTotalCount(self):
        return self.__count

    

    def GetBoardTimelineAsString(self, board):
        timeline = self.GetBoardTimeline(board)
        result = self.__timelineAsString(timeline)
        return result

    def __timelineAsString(self, timeline):
        timelineString = ''
        for date, count in timeline.YearlyDecisions.items():
            dateString = date.strftime('%Y/%m/%d')
            countString = str(count)
            timelineString += dateString + '::' + countString + ';'
        return timelineString


    def GetBoardTimelineFromString(self, string):
        return self.__timelineFromString(string)


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


class BoardTimelineAnalysis(object):

    def __init__(self, board):
        self.Board = board
        self.YearlyDecisions = None

    def MakeFromTimeline(self, timeline):
        self.YearlyDecisions = self.__accumulateTimelineYears(timeline)

    #to do
    #region do we need these?
    def MakeFromYearlyDecisions(yearlyDecisions):
        self.YearlyDecisions = yearlyDecisions


    def __getEarliestDecisionOfMonth(self, dt:datetime):
        return self.__getFirstOfMonth(dt)

    def __getLastestDecisionOfMonth(self, dt:datetime):
        return self.__getFirstOfMonth(dt, descending=True)

    def __getFirstOfMonth(self, dt:datetime, descending=False):
        sorter = 'DecisionDate'
        if descending: 
            sorter = '-DecisionDate'
        decisions = DecisionModelProxy.GetBibliographyFiltered(
           Board = self.Board,
           DecisionDate__range = (
              DateHelpers.FirstOfThisMonth(dt), 
              DateHelpers.EndOfThisMonth(dt))).order_by(sorter)
        return decisions.first().CaseNumber, decisions.first().DecisionDate
    #endregion

    def __accumulateTimelineYears(self, timeline):
        yearlyDecisions = {}
        decisions = DecisionModelProxy.GetAllForBoardOrderedByDecisionDate(self.Board)
        firstDate = decisions.first().DecisionDate
        lastDate = decisions.last().DecisionDate
        for year in DateHelpers.YearIterator(firstDate, lastDate):
            count = 0
            for month in DateHelpers.MonthIteratorOneYear(year):
                count += timeline.get(month, 0)
            yearlyDecisions[year] = count
        return yearlyDecisions


class BoardAnalyser(Analyser):

    def __init__(self):
        self.__cache = {}


    def GetBoardAnalysis(self, board):
        if board in self.__cache:
            return self.__cache[board]

        analysis = self.__analyseBoard(board)
        self.__cache[board] = analysis

    def __analyseBoard(self, board):
        
        boardDecisions = DecisionModelProxy.GetAllForBoardOrderedByDecisionDate(board)
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

        result =  {
            'count': count, 
            'early': early, 
            'late': late, 
            'ipctop': ipcTop5, 
            'articletop': articleTop5, 
            'citationtop': citationTop5
            }

        return result

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


    def GetSavableBoardAnalysis(self, board):
        analysis = self.GetBoardAnalysis(board)

        earlyList = [str(x.pk) for x in analysis['early']]
        earlySavable = ','.join(earlyList)

        lateList = [str(x.pk) for x in analysis['late']]
        lateSavable = ','.join(lateList)

        ipcString = self.__stringIntDecimalToString(analysis['ipctop'])
        articleString = self.__stringIntDecimalToString(analysis['articletop'])

        citationList = [(str(x.pk), y) for (x, y) in analysis['citationtop']]
        citationString = self.__stringIntToString(citationList)

        result =  {
            'count': analysis['count'], 
            'early': earlySavable, 
            'late': lateSavable, 
            'ipctop': ipcString,  
            'articletop': articleString, 
            'citationtop': citationString
            }

        return result

    
    def __stringIntDecimalToString(self, tripleList):
        resultString = ''
        for (string, integer, decimal) in tripleList:
             resultString += string + ',' + str(integer) + ',' + str(decimal) + ';'
        return resultString
    
    def __stringIntToString(self, pairList):
        resultString = ''
        for (string, integer) in pairList:
             resultString += string + ',' + str(integer) + ';'
        return resultString


    def ParseSavableBoardAnalysis(self, savableAnalysis):
        
        citationList = self.__stringIntFromString(savableAnalysis['citationtop'])

        result =  {
            'count': savableAnalysis['count'], 
            'early': self.__decisionListFromPkString(savableAnalysis['early']), 
            'late': self.__decisionListFromPkString(savableAnalysis['late']), 
            'ipctop': self.__stringIntDecimalFromString(savableAnalysis['ipctop']), 
            'articletop': self.__stringIntDecimalFromString(savableAnalysis['articletop']), 
            'citationtop': self.__pkValueToDecisionValue(citationList),
            }

        return result

    def __decisionListFromPkString(self, string):
        if not string:
            return []
        pkList = [int(x) for x in string.split(',')]
        result = []
        for pk in pkList:
            decision = DecisionModelProxy.GetDecisionFromPrimaryKey(pk)
            if decision:
                result.append(decision)
        return result

    def __pkValueToDecisionValue(self, pairs):
        result = []
        for (pk, value) in pairs:
            decision = DecisionModelProxy.GetDecisionFromPrimaryKey(pk)
            if decision:
                result.append((decision, value))
        return result


    def __stringIntDecimalFromString(self, string):
        if not string:
            return []
        resultList = []
        for triple in string.split(';'):
            if not triple:
                continue
            tripleList = triple.split(',')
            resultList.append((tripleList[0], int(tripleList[1]), Decimal(tripleList[2])))
        return resultList
    
    def __stringIntFromString(self, string):
        if not string:
            return []
        resultList = []
        for pair in string.split(';'):
            if not pair:
                continue
            pairList = pair.split(',')
            resultList.append((pairList[0], int(pair[1])))
        return resultList




class PublishedDecisionTimelineAnalyser(Analyser):
    """description of class"""

    def AnalyseAllBoardsPublishedDecisionTimeline(self):
        boardanalyses = []
        for board in self.__boards:
            analysis = self.AnalyseBoardPublishedDecisionTimeline(board)
            boardanalyses.append(analysis)
        return boardanalyses

    def AnalyseBoardPublishedDecisionTimeline(self, board):
        if not self.__analysed:
            self.AnalysePublishedDecisionTimelines()
        if board not in self.__boards:
            return None
        analysis = BoardTimelineAnalysis(board)
        analysis.MakeFromTimeline(self. __timelines[board])
        return analysis
    
    def AnalysePublishedDecisionTimelines(self):
        if self.__analysed:
            return

        self.ObjectCount = DecisionModelProxy.GetDistinctBibliographiesCount()
        orderedObjects = DecisionModelProxy.GetAllOrderedByDecisionDate()
        startDate = orderedObjects.first().DecisionDate
        endDate = orderedObjects.last().DecisionDate

        # get all boards and their timelines
        boards = []
        timelines = {}
        count = 0
        for dt in DateHelpers.MonthIterator(startDate, endDate):
            cases = DecisionModelProxy.GetAllInDateRange(dt, DateHelpers.EndOfThisMonth(dt))
                                
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
        self.__boards = []
        self.__timelines = {}
        self.__analysed = False
        self.__earliestdate = None
        self.__latestdate = None


class IPCAnalyser(Analyser):

    def IpcFrequency(self, decisions):
        return self.GetAttributeFrequency('IPC', decisions)

    def IpcFrequencyForBoard(self, board):
        decisions = DecisionModelProxy.GetAllForBoard(board)
        return self.IpcFrequency(decisions)
        

class ProvisionAnalyser(Analyser):

    def ArticleFrequency(self, decisions):
        return self.GetAttributeFrequency('Articles', decisions)

    def ArticleFrequencyForBoard(self, board):
        decisions = DecisionModelProxy.GetAllForBoard(board)
        return self.ArticleFrequency(decisions)
    
    def RuleFrequency(self, decisions):
        return self.GetAttributeFrequency('Rules', decisions)

    def RuleFrequencyForBoard(self, board):
        decisions = DecisionModelProxy.GetAllForBoard(board)
        return self.RuleFrequency(decisions)


class CitationAnalyser(Analyser):
    
    def CitationFrequency(self, decisions):
        result = {}
        for decision in decisions:
            result[decision] = DecisionModelProxy.GetCitingCasesFromCaseNumber(decision.CaseNumber).count()
        return result

    def CitationFrequencyForBoard(self, board):
        decisions = DecisionModelProxy.GetAllForBoard(board)
        return self.CitationFrequency(decisions)







