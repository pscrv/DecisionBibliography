from app.DBProxy import DecisionModelProxy

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


def IpcFrequency(decisions):
    return __getAttributeFrequency('IPC', decisions)

def IpcFrequencyForBoard(board):
    decisions = DecisionModelProxy.GetAllForBoard(board)
    return IpcFrequency(decisions)



def ArticleFrequency(decisions):
    return __getAttributeFrequency('Articles', decisions)

def ArticleFrequencyForBoard(board):
    decisions = DecisionModelProxy.GetAllForBoard(board)
    return ArticleFrequency(decisions)
    
def RuleFrequency(decisions):
    return __getAttributeFrequency('Rules', decisions)

def RuleFrequencyForBoard(board):
    decisions = DecisionModelProxy.GetAllForBoard(board)
    return RuleFrequency(decisions)


    
def CitationFrequency(decisions):
    result = {}
    for decision in decisions:
        result[decision] = DecisionModelProxy.GetCitingCasesFromCaseNumber(decision.CaseNumber).count()
    return result

def CitationFrequencyForBoard(board):
    decisions = DecisionModelProxy.GetAllForBoard(board)
    return CitationFrequency(decisions)
