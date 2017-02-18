
from Decisions.models import NullTextModel, NullSupplementaryModel

class DecisionProxy:
    
    def __init__(self, bibliographymodel):
        self.__bibliography = bibliographymodel
        self.__texts = bibliographymodel.TextModel if hasattr(bibliographymodel, 'TextModel') else NullTextModel()
        self.__supplement = bibliographymodel.SupplementModel if hasattr(bibliographymodel, 'SupplementModel') else NullSupplementaryModel()
               
        for part in (self.__bibliography, self.__texts, self.__supplement):
            self.__dict__.update(part.__dict__)
        self.pk = self.id
    

    def __getattribute__(self, attr):
        if attr in ['Facts', 'Reasons', 'Order']:
            return object.__getattribute__(self, attr).split('\n\n')
        return object.__getattribute__(self, attr)

        

    @property
    def HasText(self):
        return not isinstance(self.__texts, NullTextModel)

    def __str__(self):
        return self.CaseNumber

    def __repr__(self):
        return 'DecisionProxy: {}'.format(self.CaseNumber)

