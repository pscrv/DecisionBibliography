import re

from decimal import Decimal

from app.DBProxy import DecisionModelProxy


def IpcMainFrequencyForBoard_TopN_withPercentage(board, n, total):
    frequency = IpcMainFrequencyForBoard(board)
    topN = __topNFromDictionaryWithPercentage(frequency, n, total)
    return topN

def IpcMainFrequencyForBoard(board):
    frequency = IpcFrequencyForBoard(board)
    return __ipcToIpcMain(frequency)

def IpcMainFrequency(decisions):
    frequencies = IpcFrequency(decisions)
    mainFrequencies = __ipcToIpcMain(frequencies)
    return mainFrequencies

def IpcFrequencyForBoard(board):
    decisions = DecisionModelProxy.GetAllForBoard(board)
    return IpcFrequency(decisions)

def IpcFrequency(decisions):
    return __getAttributeFrequency('IPC', decisions)

def __ipcToIpcMain(ipcdict):
    mainFrequencies = {}
    finder = re.compile(r'(.*)/(.*)')
    for cl in ipcdict:
        found = re.search(finder, cl)
        if not found:
            continue
        main = found.group(1)
        mainFrequencies[main] = mainFrequencies.get(main, 0) + ipcdict[cl]
    return mainFrequencies



def ArticleFrequencyForBoard_TopN_withPercentage(board, n, total):
    frequency = ArticleFrequencyForBoard(board)
    topN = __topNFromDictionaryWithPercentage(frequency, n, total)
    return topN

def ArticleFrequencyForBoard(board):
    decisions = DecisionModelProxy.GetAllForBoard(board)
    return ArticleFrequency(decisions)

def ArticleFrequency(decisions):
    return __getAttributeFrequency('Articles', decisions)

    
def RuleFrequency(decisions):
    return __getAttributeFrequency('Rules', decisions)

def RuleFrequencyForBoard(board):
    decisions = DecisionModelProxy.GetAllForBoard(board)
    return RuleFrequency(decisions)


def ArticleFrequencyForBoard_TopN(board, n):
    frequency = CitationFrequencyForBoard(board)
    topN = __topNFromDictionary(frequency, n)
    return topN


def CitationFrequency(decisions):
    result = {}
    for decision in decisions:
        result[decision] = DecisionModelProxy.GetCitingCasesFromCaseNumber(decision.CaseNumber).count()
    return result

def CitationFrequencyForBoard(board):
    decisions = DecisionModelProxy.GetAllForBoard(board)
    return CitationFrequency(decisions)


def __getAttributeFrequency(attribute, decisions):
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

    
def __topNFromDictionaryWithPercentage(dict, n, total):
    keyList = sorted(dict.keys(), key=(lambda k: dict[k]), reverse = True)[:n]
    return [ (k, dict[k], round(Decimal(100 * dict[k] / total), 2)) for k in keyList]

def __topNFromDictionary(dict, n):    
    keyList = sorted(dict.keys(), key=(lambda k: dict[k]), reverse = True)[:n]
    return [ (k, dict[k]) for k in keyList]
