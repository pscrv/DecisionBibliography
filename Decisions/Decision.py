
from Decisions.models import DecisionBibliographyModel, NullBibliographyModel, DecisionTextModel, NullTextModel, DecisionSupplementaryModel, NullSupplementaryModel

class DecisionProxy:

    def __init__(self, bibliographymodel, textmodel = NullTextModel(), supplementarymodel = NullSupplementaryModel() ):
        if not isinstance(textmodel, NullTextModel):
            assert textmodel.Bibliography == bibliographymodel, 'bibliographymodel and textmodel do not match'
        if not isinstance(supplementarymodel, NullSupplementaryModel):
            assert supplementarymodel.Bibliography == bibliographymodel, 'bibliographymodel and supplementarymodel do not match'


        self.__bibliography = bibliographymodel
        #self.__texts = textmodel
        #self.__supplement = supplementarymodel
        if hasattr(self.__bibliography, 'TextModel'):
            self.__texts = bibliographymodel.TextModel 
        else:
            self.__texts =  NullTextModel()
        if hasattr(self.__bibliography, 'SupplementModel'):
            self.__supplement = bibliographymodel.SupplementModel 
        else:
           self.__supplement = NullSupplementaryModel()

       
        for part in (self.__bibliography, self.__texts, self.__supplement):
            self.__dict__.update(part.__dict__)
        for part in ['Facts', 'Reasons', 'Order']:
            self.__dict__[part] = self.__texts.__dict__[part].split('\n\n')
        self.pk = self.__bibliography.pk


    @property
    def HasText(self):
        return not isinstance(self.__texts, NullTextModel)

    def __str__(self):
        return self.CaseNumber

    def __repr__(self):
        return 'DecisionProxy: {}'.format(self.CaseNumber)


