import abc
from Classifiers.TrainingTexts import Texts

class TrainingTextProvider(abc.ABC):

    @abc.abstractmethod
    def GetFeatureText(self):
        pass
    
    @abc.abstractmethod
    def GetNonFeatureText(self):
        pass

    @abc.abstractmethod
    def GetStopwords(self):
        pass
