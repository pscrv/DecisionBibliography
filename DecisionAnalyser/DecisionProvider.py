import abc

class DecisionProvider(abc.ABC):

    @abc.abstractmethod
    def GetDecisions(self, classname):
        pass


class SimpleDecisionProvider(DecisionProvider):

    def GetDecisions(self, classname):
        if classname.lower() == 'restitutio':
            decisionNumbers = ['T 0027/86', 'J 0026/88', 'T 0613/93', 'J 0008/91']
            from app.DBProxy import DecisionModelProxy
            return [DecisionModelProxy.GetDecisionListFromCaseNumber(x) for x in decisionNumbers]
        return None