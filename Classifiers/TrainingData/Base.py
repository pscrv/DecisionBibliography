import abc

class BinaryTrainingDataBase(abc.ABC):

    def __init__(self, name):
        self._name = name
        self._classes = [name, 'other']
        self._features = []
        self._testTexts = []
        self._texts = {
            name : [],
            'other' : []
            }


    def GetTrainingTexts(self, cl):
        return self._texts.get(cl, [])

    def GetClassProportion(self, cl):
        texts = self.GetTrainingTexts(cl)
        return len(texts) / self.TotalTextCount

    @property
    def Classes(self):
        return self._classes

    @property
    def Features(self):
        return self._features

    @property
    def FeatureCount(self):
        return len(self._features)

    @property
    def PositiveData(self):
        return self._positiveTexts

    @property
    def NegativeData(self):
        return self._negativeTexts

    @property
    def TestData(self):
        return self._testTexts
    
    @property
    def TotalTextCount(self):
        return len(self._texts[self._name]) + len(self._texts['other'])

    @property
    def PositiveProportion(self):
        return len(self._texts[self._name]) / self.TotalTextCount

    @property
    def NegativeProportion(self):
        return len(self._texts['other']) / self.TotalTextCount

    def SplitTextsBy(self, cl, term):
        if cl == self._name:
            source = self.PositiveData
        else:
            source = self.NegativeData
        return (
            ' '.join([x for x in source if term in x]),
            ' '.join([x for x in source if term not in x]),
            )

