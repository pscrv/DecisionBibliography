import abc
from Classifiers.Classifier_Setup import Texts

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
