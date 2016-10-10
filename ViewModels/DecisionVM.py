from abc import ABC, abstractmethod

from django.db.models import F

from app.DBProxy import DecisionModelProxy
from app.DBPopulator import TextGetter


class DecisionViewModel(ABC):


    @abstractmethod
    def _setDecisionToShow(self):
        pass

    @abstractmethod
    def _needMessage(self):
        pass

    @abstractmethod
    def _needUnfoundContext(self):
        pass


    
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

    def _downloadText(self, decision):   
        textGetter = TextGetter()
        text = textGetter.Get_Text(decision)
        return text

    def _getText(self, decision):
        text = DecisionModelProxy.GetTextFromDecision(decision)
        if not text:
            text = self._downloadText(decision)
        if not text:
            text = DecisionModelProxy.GetErrorText()
        return text

    

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
        self.Context = {
            'title': '',
            'message': self._message,
            }

    def _setFullContext(self):
        self._setDecisionToShow() 
        sameDate = self._decisions.filter(DecisionDate = self._decisionToShow.DecisionDate)
        otherLanguages = sameDate.exclude(pk = self._decisionToShow.pk)
        otherVersions = self._decisions.exclude(DecisionDate = self._decisionToShow.DecisionDate)      
        
        citingDecisions = self._getCitingDecisionsAsTimeline(self._decisionToShow)
        citedDecisions = self._getCitedDecisions(self._decisionToShow)
        text = self._getText(self._decisionToShow)
        
        self.Context = {
            'title': '',
            'message': self._message,
            'decision': self._decisionToShow,
            'citedDecisions': citedDecisions,
            'citingyears': citingDecisions['years'],
            'citingtl': citingDecisions['timeline'],
            'citingCount': citingDecisions['count'],
            'factsHeader': text.FactsHeader,
            'facts': text.Facts.split('\n\n'),
            'reasonsHeader': text.ReasonsHeader,
            'reasons': text.Reasons.split('\n\n'),
            'orderHeader': text.OrderHeader,
            'order': text.Order.split('\n\n'),
            'languageversions': otherLanguages,
            'otherversions': otherVersions,
            }


class DecisionListViewModel(DecisionViewModel):
    
    def __init__(self, decisions, pk = None, msg = ''):
        self._decisions = decisions
        self._pk = pk
        self._message = msg
        self._decisionToShow = None

        self._setup()        

  
    def _needMessage(self):
        return not self._decisions

    def _setDecisionToShow(self):
        if self._pk:
            self._decisionToShow = self._decisions.filter(pk = self._pk).first()
        else:
            decisionsInPrLang = self._decisions.filter(DecisionLanguage = F('ProcedureLanguage'))
            if decisionsInPrLang:
                self._decisionToShow = decisionsInPrLang.order_by('-DecisionDate')[0]
            else:
                self._decisionToShow = self._decisions[0]

    def _needUnfoundContext(self):
        return not self._decisions






#region SingleDecisionViewModel  - temporary keep
#class SingleDecisionViewModel(DecisionViewModel):
    #def __init__(self, decision, msg = ''):
    #    self._decision = decision
    #    self._message = msg
    #    self._decisionToShow = None
    #    if decision:
    #        self._pk = decision.pk
    #    else:
    #        self._pk = None

    #    self._setup()
       
        
    #def _setDecisionToShow(self):
    #    return self._decision

    #def _needMessage(self):
    #    return not self._decision

    #def _needUnfoundContext(self):
    #    return not self._decision

#endregion
  
