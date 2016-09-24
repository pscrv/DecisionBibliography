from app.models import DecisionBibliographyModel, DecisionTextModel
from app.DBPopulator import TextGetter

class SingleDecisionViewModel(object):
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

        self.Context = {
            'title': 'DecisionView',
            'message': message,
            'decision': decision,
            'citedDecisions': self.__getCitedDecisions(decision),
            'citingDecisions': citingDecisions,
            'citingCount': citingDecisions.count(),
            'factsHeder': text.FactsHeader,
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
        citing = DecisionBibliographyModel.objects.FilterOnlyPrLanguage(CitedCases=decision.CaseNumber).all()
        return citing

    def __downloadText(self, decision):   
        textGetter = TextGetter()
        return textGetter.Get_Text(decision)




