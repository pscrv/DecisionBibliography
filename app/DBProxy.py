from abc import ABC, abstractmethod

from django.db.models import F
from app.models import DecisionBibliographyModel, DecisionTextModel

class DBProxy(ABC):
    """abstract base class for DB access"""

    @abstractmethod
    def GetDefaultAndOthersFromCaseNumber():
        pass


class DecisionModelProxy(DBProxy):
    """proxy class for accessing DecisionBibliographyModel and DecisionTextModel """


    def GetDefaultAndOthersFromCaseNumber(cn):

        decisionList = DecisionBibliographyModel.objects.filter(CaseNumber = cn)
        default = decisionList.filter(DecisionLanguage =  F('ProcedureLanguage')).first()
        others = decisionList.exclude(pk = default.pk)
        return default, others

