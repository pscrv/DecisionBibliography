
from Decisions.models import DecisionBibliographyModel, NullBibliographyModel, DecisionTextModel, NullTextModel

class DecisionProxy:

    def __init__(self, bibliographymodel, textmodel):
        assert textmodel.Bibliography == bibliographymodel, 'bibliographymodel and textmodel do not match'

        self.__bibliography = bibliographymodel
        self.__texts = textmodel


        for part in (self.__bibliography, self.__texts):
            self.__dict__.update(part.__dict__)
        self.__dict__['pk'] = self.__bibliography.pk

    @property
    def HasText(self):
        return not isinstance(self.__texts, NullTextModel)

    def __str__(self):
        return self.CaseNumber


