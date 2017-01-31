from abc import ABC, abstractmethod

from Decisions.models import DecisionBibliographyModel, DecisionTextModel, NullTextModel
from Decisions.Decision import DecisionProxy


class DBProxy2(ABC):
    """abstract base class for DB access"""
    
    @abstractmethod
    def GetFilteredOnBibliographyKeywords(**kwargs):
        pass

    
    @abstractmethod
    def GetFilteredOnTextKeywords(**kwargs):
        pass



class DecisionModelProxy(DBProxy2):

    def GetFilteredOnBibliographyKeywords(**kwargs):
        result_qset = DecisionBibliographyModel.objects.filter(**kwargs)
        result_list = []
        for bibliography in result_qset:
            try:
                text = DecisionTextModel.objects.get(Bibliography = bibliography)
            except DecisionTextModel.DoesNotExist:
                text = NullTextModel()
                text.Bibliography = bibliography

            result_list.append(DecisionProxy(bibliography, text))

        return result_list

    def GetFilteredOnTextKeywords(**kwargs):
        result_qset = DecisionTextModel.objects.filter(**kwargs)
        #result_list = []
        #for text in result_qset:
        #    bibliography = text.Bibliography
        #result_list.append(DecisionProxy(bibliography, text))
        #return result_list
        return [DecisionProxy(t.Bibliography, t) for t in result_qset]


