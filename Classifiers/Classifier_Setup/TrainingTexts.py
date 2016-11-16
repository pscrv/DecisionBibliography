from Classifiers.Classifier_Setup import Texts
from Classifiers.Classifier_Setup.TrainingTextBase import TrainingTextProvider

class TrainingTexts(TrainingTextProvider):
    
    def __init__(self, keyword):
        self.__texts = Texts.GetText(keyword)
        self.__otherTexts = Texts.GetText('-' + keyword)
        self.__stopwords = Texts.GetStopwords()


    def GetFeatureText(self):
        return self.__texts
    
    def GetNonFeatureText(self):
        return self.__otherTexts

    def GetStopwords(self):
        return self.__stopwords
