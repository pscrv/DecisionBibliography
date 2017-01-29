
from Decisions.models import DecisionBibliographyModel, NullBibliographyModel, DecisionTextModel, NullTextModel



class DecisionProxy:
    
    def __init__(self, casenumber, language = None):

        if language is None:
            bibliography = DecisionBibliographyModel.objects.FilterOnlyPrLanguage(CaseNumber = casenumber).first()
        else:
            bibliography = DecisionBibliographyModel.objects.filter(CaseNumber = casenumber, DecisionLanguage = language).first()

        if bibliography is None:
            self.__bibliography = NullBibliographyModel()
            self.__texts = NullTextModel()
        else: 
            self.__bibliography = bibliography
            texts = DecisionTextModel.objects.filter(decision = self.__bibliography).first()
            if texts is not None:
                self.__texts = texts
            else:
                self.__texts = NullTextModel()


        for part in (self.__bibliography, self.__texts):
            self.__dict__.update(part.__dict__)


