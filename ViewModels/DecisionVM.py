from app.DBProxy import DecisionModelProxy
from app.DBPopulator import TextGetter

    
class SingleDecisionViewModel(object):
    def __init__(self, decision, others = None, msg = ''):
        message = msg

        if message == '' and not decision:
            message = 'Not found'

        if not decision:
            self.Context = {
                'title': '',
                'message': message,
                }
            return

        citingDecisions = self.__getCitingDecisionsAsTimeline(decision)
        text = self.__getText(decision)

        self.Context = {
            'title': '',
            'message': message,
            'decision': decision,
            'citedDecisions': self.__getCitedDecisions(decision),
            'citingyears': citingDecisions['years'],
            'citingtl': citingDecisions['timeline'],
            'citingCount': citingDecisions['count'],
            'factsHeader': text.FactsHeader,
            'facts': text.Facts.split('\n\n'),
            'reasonsHeader': text.ReasonsHeader,
            'reasons': text.Reasons.split('\n\n'),
            'orderHeader': text.OrderHeader,
            'order': text.Order.split('\n\n'),
            'otherversions': others,
            }
        

    def __getCitedDecisions(self, decision):
        citedDecisions = []
        if not decision:
            return citedDecisions
        if decision.CitedCases == "":
            return citedDecisions
        for case in decision.CitedCases.split(','):
            case = case.strip()
            dec = DecisionModelProxy.GetRepresentativeForCaseNumber(case)
            if dec:
                citedDecisions.append(dec)
        return citedDecisions

    def __getCitingDecisions(self, decision):
        citing = DecisionModelProxy.GetCitingCasesFromCaseNumber(decision.CaseNumber)
        return citing

    def __getCitingDecisionsAsTimeline(self, decision):
        citing = self.__getCitingDecisions(decision)
        if not citing:
            return {'count': 0, 'years': [], 'timeline': []}

        yeardictionary = {}
        for citer in citing:
            year = citer.DecisionDate.year
            yearlist = yeardictionary.get(year, [])
            yearlist.append(citer.CaseNumber.replace(' ', '\u00A0'))
            yeardictionary[year] = yearlist

        timeline = []
        startyear = min(yeardictionary)
        endyear = max(yeardictionary)
        years = range(startyear, endyear + 1)
        for y in years:
            timeline.append(yeardictionary.get(y, []))

        return {'count': len(citing), 'years': years, 'timeline' : timeline}

    def __downloadText(self, decision):   
        textGetter = TextGetter()
        text = textGetter.Get_Text(decision)
        return text

    def __getText(self, decision):
        text = DecisionModelProxy.GetTextFromDecision(decision)
        if not text:
            text = self.__downloadText(decision)
        if not text:
            text = DecisionModelProxy.GetErrorText()
        return text



