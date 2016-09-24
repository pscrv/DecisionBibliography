import re
from app.models import DecisionBibliographyModel as DB
from app.DBAnalyser import IPCAnalyser, ProvisionAnalyser, CitationAnalyser

class  BoardViewModel(object):
    
    def __init__(self, bd):
        boardDecisions =  DB.objects.FilterOnlyPrLanguage(Board = bd).order_by('DecisionDate')
        count = boardDecisions.count()
        early = boardDecisions[:5]
        late = boardDecisions[count-5:]

        ipcAnalyser = IPCAnalyser()
        ipcFrequencies = ipcAnalyser.IpcFrequencyForBoard(bd)
        ipcMainFrequencies = self.__ipcToIpcMain(ipcFrequencies)
        ipcTop5 = self.__topNFromDictionaryWithPercentage(ipcMainFrequencies, 5, count)

        provisionAnalyser = ProvisionAnalyser()
        articleFrequencies = provisionAnalyser.ArticleFrequencyForBoard(bd)
        articleTop5 = self.__topNFromDictionaryWithPercentage(articleFrequencies, 5, count)

        citationAnalyser = CitationAnalyser()
        citationFrequencies = citationAnalyser.CitationFrequencyForBoard(bd)
        citationTop5 = self.__topNFromDictionary(citationFrequencies, 5)

        self.Context = {
            'board' : bd,
            'count' : count,
            'earliest': early,
            'latest': late,
            'ipc' : ipcTop5,
            'provisions': articleTop5,
            'citations': citationTop5,
            'title': 'Board ' + bd
            }


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
        from decimal import Decimal
        keyList = sorted(dict.keys(), key=(lambda k: dict[k]), reverse = True)[:n]
        return [ (k, dict[k], round(Decimal(100 * dict[k] / total), 2)) for k in keyList]

    def __topNFromDictionary(self, dict, n):    
        keyList = sorted(dict.keys(), key=(lambda k: dict[k]), reverse = True)[:n]
        return [ (k, dict[k]) for k in keyList]

    def __appendPercentage (self, pairList, total):
        from decimal import Decimal
        return [ (x, y, round(Decimal(100 *y / total), 2)) for (x, y) in pairList]



