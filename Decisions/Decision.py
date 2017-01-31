
from Decisions.models import DecisionBibliographyModel, NullBibliographyModel, DecisionTextModel, NullTextModel

class DecisionProxy:
    
    #def __init__(self, casenumber, language = None):

    #    if language is None:
    #        bibliography = DecisionBibliographyModel.objects.FilterOnlyPrLanguage(CaseNumber = casenumber).first()
    #    else:
    #        bibliography = DecisionBibliographyModel.objects.filter(CaseNumber = casenumber, DecisionLanguage = language).first()

    #    if bibliography is None:
    #        self.__bibliography = NullBibliographyModel()
    #        self.__texts = NullTextModel()
    #    else: 
    #        self.__bibliography = bibliography
    #        texts = DecisionTextModel.objects.filter(decision = self.__bibliography).first()
    #        if texts is None:
    #            self.__texts = NullTextModel()
    #        else:
    #            self.__texts = texts
    

        #for part in (self.__bibliography, self.__texts):
        #    self.__dict__.update(part.__dict__)
        #    self.__dict__[pk] = self.__bibliography.pk

    def __init__(self, bibliographymodel, textmodel):
        assert textmodel.Bibliography == bibliographymodel, 'bibliographymodel and textmodel do not match'

        self.__bibliography = bibliographymodel
        self.__texts = textmodel


        for part in (self.__bibliography, self.__texts):
            self.__dict__.update(part.__dict__)
        self.__dict__['pk'] = self.__bibliography.pk


