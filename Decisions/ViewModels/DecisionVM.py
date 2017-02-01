from django.db.models import F

from Decisions.ViewModels.Base import VMBase
from Decisions.DBProxy import DecisionModelProxy
from Decisions.DBPopulator import TextGetter

class DecisionViewModel(VMBase):

    def __init__(self, decisions, pk = None, msg = '', highlightterms = []):
        super(DecisionViewModel, self).__init__()

        self._decisions = decisions
        self._message = msg
        self._decisionToShow = None
        self._highlightterms = highlightterms
        
        self._pk = int(pk) if pk else None

        self._setup()



    def _setup(self):
        if self._message == '' and self._needMessage():
            self._message = 'Not found'        
        self._setContext()

    
    def _setContext(self):
        if self._needUnfoundContext():
            self._setContextForUnfound()
        else:
            self._setFullContext()


    def _setContextForUnfound(self):
        self.Context.update( {
            'title': '',
            'message': self._message,
            } )


    def _setFullContext(self):
        self._setDecisionToShow() 
        sameDate = [x for x in self._decisions if x.DecisionDate == self._decisionToShow.DecisionDate]
        otherLanguages = [x for x in sameDate if not x.pk == self._decisionToShow.pk]
        otherVersions = [x for x in self._decisions if not x.DecisionDate == self._decisionToShow.DecisionDate]
        
        citingDecisions = self._getCitingDecisionsAsTimeline(self._decisionToShow)
        citedDecisions = self._getCitedDecisions(self._decisionToShow)        
        self.__downloadTextIfNeeded(self._decisionToShow)

        #TODO: modifiy this to send just 'decision', which now contains
        #facts, reasons, etc.
        #Need to modify template for that.
        self.Context.update( {
            'title': '',
            'message': self._message,
            'decision': self._decisionToShow,
            'citedDecisions': citedDecisions,
            'citingyears': citingDecisions['years'],
            'citingtl': citingDecisions['timeline'],
            'citingCount': citingDecisions['count'],
            'factsHeader': self._decisionToShow.FactsHeader,
            'facts': self._decisionToShow.Facts.split('\n\n'),
            'reasonsHeader': self._decisionToShow.ReasonsHeader,
            'reasons': self._decisionToShow.Reasons.split('\n\n'),
            'orderHeader': self._decisionToShow.OrderHeader,
            'order': self._decisionToShow.Order.split('\n\n'),
            'languageversions': otherLanguages,
            'otherversions': otherVersions,
            'highlightterms': self._highlightterms,
            } )
        

    def _setDecisionToShow(self):
        if self._pk:
            self._decisionToShow = [x for x in self._decisions if x.pk == self._pk][0]
        else:            
            decisionsInPrLang = [x for x in self._decisions if x.DecisionLanguage == x.ProcedureLanguage]
            if decisionsInPrLang != []:
                self._decisionToShow = min(decisionsInPrLang, key = lambda x: x.DecisionDate)
            else:
                self._decisionToShow = self._decisions[0]


    def _needMessage(self):
        return not self._decisions


    def _needUnfoundContext(self):
        return not self._decisions

    
    def _getCitedDecisions(self, decision):
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

    def _getCitingDecisions(self, decision):
        citing = DecisionModelProxy.GetCitingCasesFromCaseNumber(decision.CaseNumber)
        return citing

    def _getCitingDecisionsAsTimeline(self, decision):
        citing = self._getCitingDecisions(decision)
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


    #TODO: make this nice
    def __downloadTextIfNeeded(self, decision):
        if decision.HasText:
            return
        textGetter = TextGetter()
        text = textGetter.Get_Text(decision)
        decision.FactsHeader = text.FactsHeader
        decision.Facts = text.Facts
        decision.ReasonsHeader = text.ReasonsHeader
        decision.Reasons = text.Reasons
        decision.OrderHeader = text.Order

