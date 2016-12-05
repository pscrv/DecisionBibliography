from Classifiers.TrainingTexts import Texts
from Classifiers.TrainingTexts.TrainingTextBase import TrainingTextProvider
from Helpers import TextHelpers

class TrainingTexts(TrainingTextProvider):
    
    def __init__(self, keyword):
        self.__stopwords = Texts.GetStopwords()

        self.__texts = Texts.GetText(keyword)
        self.__textWordCount = TextHelpers.countwords(self.__texts)
        self.__reducedTexts = TextHelpers.removeWords(self.__texts, self.__stopwords)

        self.__otherTexts = Texts.GetText('-' + keyword)
        self.__otherTextsWordCount = TextHelpers.countwords(self.__otherTexts)
        self.__reducedOtherTexts = TextHelpers.removeWords(self.__otherTexts, self.__stopwords)


    def GetFeatureText(self):
        return self.__texts

    def GetFeatureTextWordCount(self):
        return self.__textWordCount
    
    def GetReducedFeatureText(self):
        return self.__reducedTexts


    def GetNonFeatureText(self):
        return self.__otherTexts
    
    def GetNonFeatureTextWordCount(self):
        return self.__otherTextsWordCount
    
    def GetReducedNonFeatureText(self):
        return self.__reducedOtherTexts#

    
    def GetStopwords(self):
        return self.__stopwords
