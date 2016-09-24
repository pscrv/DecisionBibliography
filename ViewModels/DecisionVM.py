from app.models import DecisionBibliographyModel

class SingleDecisionViewModel(object):
    def __init__(self,decision, msg = ''):
        message = msg
        if message == '' and not decision:
            message = 'Not found'
        self.Context = {
            'title': 'DecisionView',
            'message': message,
            'decision': decision,
            'citedDecisions': self.__getCitedDecisions(decision),
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