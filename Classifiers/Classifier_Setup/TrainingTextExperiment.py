from Classifiers.Classifier_Setup import Texts
from Classifiers.Classifier_Setup.TrainingTextBase import TrainingTextProvider

class TrainingTexts(TrainingTextProvider):
    

    def GetFeatureText(self):
        return self.__texts
    
    def GetNonFeatureText(self):
        return self.__otherTexts

    def GetStopwords(self):
        return self.__stopwords

    def GetExtrinsicTerms(self):
        return self.__extrinsicTerms



    def __init__(self, keyword : str, extrinsicterms):
        self.__texts = Texts.GetText(keyword)
        self.__otherTexts = Texts.GetText('-' + keyword)
        self.__stopwords = Texts.GetStopwords()
        self.__extrinsicTerms = {x for x in extrinsicterms}
