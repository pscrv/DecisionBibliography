from app.models import DecisionBibliographyModel, DecisionTextModel
from app.DBPopulator import TextGetter

class SingleDecisionViewModel_old(object):
    def __init__(self, decision, msg = ''):
        message = msg

        if message == '' and not decision:
            message = 'Not found'

        if not decision:
            self.Context = {
                'title': 'DecisionView',
                'message': message,
                }
            return

        citingDecisions = self.__getCitingDecisions(decision)
        text = DecisionTextModel.objects.filter(decision = decision).first()
        if not text:
            text = self.__downloadText(decision)  
        if not text:
            text = DecisionTextModel()
            text.FactsHeader = "Decision text unavailable."
            text.Facts = ""
            text.ReasonsHeader = "Decision text unavailable."
            text.Reasons = ""
            text.OrderHeader = "Decision text unavailable."
            text.Order = ""


        self.Context = {
            'title': 'DecisionView',
            'message': message,
            'decision': decision,
            'citedDecisions': self.__getCitedDecisions(decision),
            'citingDecisions': citingDecisions,
            'citingCount': citingDecisions.count(),
            'factsHeader': text.FactsHeader,
            'facts': text.Facts.split('\n\n'),
            'reasonsHeader': text.ReasonsHeader,
            'reasons': text.Reasons.split('\n\n'),
            'orderHeader': text.OrderHeader,
            'order': text.Order.split('\n\n'),
            }
        
    def __getCitedDecisions(self, decision):
        citedDecisions = []
        if not decision:
            return citedDecisions
        if decision.CitedCases == "":
            return citedDecisions
        for case in decision.CitedCases.split(','):
            case = case.strip()
            dec = DecisionBibliographyModel.objects.GetFromCaseNumber(case)
            if dec:
                citedDecisions.append(dec)
        return citedDecisions

    def __getCitingDecisions(self, decision):
        citing = DecisionBibliographyModel.objects.FilterOnlyPrLanguage(CitedCases__contains=decision.CaseNumber).all()
        return citing

    def __downloadText(self, decision):   
        textGetter = TextGetter()
        text = textGetter.Get_Text(decision)
        if not text:
            text = DecisionTextModel(
            FactsHeader = "Decision text unavailable.",
            Facts = "",
            ReasonsHeader = "Decision text unavailable.",
            Reasons = "",
            OrderHeader = "Decision text unavailable.",
            Order = "")
        return text

    
class SingleDecisionViewModel(object):
    def __init__(self, decision, msg = ''):
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
            }
        

    def __getCitedDecisions(self, decision):
        citedDecisions = []
        if not decision:
            return citedDecisions
        if decision.CitedCases == "":
            return citedDecisions
        for case in decision.CitedCases.split(','):
            case = case.strip()
            dec = DecisionBibliographyModel.objects.GetFromCaseNumber(case)
            if dec:
                citedDecisions.append(dec)
        return citedDecisions

    def __getCitingDecisions(self, decision):
        citing = DecisionBibliographyModel.objects.FilterOnlyPrLanguage(CitedCases__contains=decision.CaseNumber).all()
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
        if not text:
            text = DecisionTextModel(
            FactsHeader = "Decision text unavailable.",
            Facts = "",
            ReasonsHeader = "Decision text unavailable.",
            Reasons = "",
            OrderHeader = "Decision text unavailable.",
            Order = "")
        return text

    def __getText(self, decision):
        text = DecisionTextModel.objects.filter(decision = decision).first()
        if not text:
            text = self.__downloadText(decision)  
        if not text:
            text = DecisionTextModel()
            text.FactsHeader = "Decision text unavailable."
            text.Facts = ""
            text.ReasonsHeader = "Decision text unavailable."
            text.Reasons = ""
            text.OrderHeader = "Decision text unavailable."
            text.Order = ""
        return text



