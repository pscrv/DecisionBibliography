from Helpers import TextHelpers
from Classifiers.Classifier_Setup.TrainingTexts import TrainingTexts
from Classifiers.Classifier_Setup.TrainingTextBase import TrainingTextProvider
from Classifiers.Classifier_Setup.SetupBase import SetupProvider


class BinaryTrainingDataBase(SetupProvider):

    def __init__(self, keyword, trainingTexts: TrainingTextProvider):
        self.__trainingTexts = trainingTexts
        self._stopwords = self.__trainingTexts.GetStopwords()
        self._extrinsicFeatures = set()
        self._extractedFeatures = set()
                
        self._name = keyword
        self._othername = 'other'

        self._texts = {
            self._name: self.__trainingTexts.GetFeatureText(),
            self._othername: self.__trainingTexts.GetNonFeatureText(),
            }



    @property
    def Classes(self):
        return [self._name, self._othername]
    
    @property
    def Features(self):
        return set.union(self._extrinsicFeatures, self._extractedFeatures)
        
    def GetTrainingTexts(self, cl):
        return self._texts.get(cl, '')

    def GetClassProportion(self, cl):
        texts = self.GetTrainingTexts(cl)
        return len(texts) / (len(self._texts[self._name]) + len(self._texts[self. _othername]))

    def GetClassProbabilities(self):
        result = {}
        for cl in self.Classes:
            result[cl] = self.GetClassProportion(cl)
        return result
    
    def GetFeatureProbabilities(self):
        features = self.Features
        featuresCount = len(features)
        featureProbabilitiesGivenClass = {}
        for cl in self.Classes:
            featureProbabilitiesGivenClass[cl] = {}
            classText = self.GetTrainingTexts(cl)
            totalWordCount = TextHelpers.countwords(classText)
            totalDivisor = totalWordCount + featuresCount

            for feature in features:
                featureOccurences = TextHelpers.countstringoccurences(feature, classText)
                prob = (1 + featureOccurences) / totalDivisor
                featureProbabilitiesGivenClass[cl][feature] = prob
        return featureProbabilitiesGivenClass

    




class BinaryTrainingDate_WithExtraction_Base(BinaryTrainingDataBase):
    
    @property
    def Features(self):
        if not self._extractedFeatures:
            self._extractFeatures()
        return super(BinaryTrainingDate_WithExtraction_Base, self).Features                


    def _extractFeatures(self):
        self.__extractFeaturesFromTexts()
        self._features = set.union(self._extrinsicFeatures, self._extractedFeatures)
        

    def __extractFeaturesFromTexts(self):
        mostFrequentWordsInFeatureTexts = self.__getNMostFrequent(
            ' '.join([x
                      for x in self.__simpleWordSplit(self._texts[self._name])
                      if x.lower() not in self._stopwords]),
            10)
        mostFrequentWordsOutsideFeatureTexts = self.__getNMostFrequent(
            ' '.join([x
                      for x in self.__simpleWordSplit(self._texts[self._othername])
                      if x.lower() not in self._stopwords]), 
            50)    
        self._extractedFeatures = {x for x in mostFrequentWordsInFeatureTexts if x not in mostFrequentWordsOutsideFeatureTexts}
        

    def __getNMostFrequent(self, text, n = 10):
        if not text:
            return {}        
        words = self.__simpleWordSplit(text)
        wordFrequencies = {}
        for word in words:
            wordFrequencies[word] = wordFrequencies.get(word, 0) + 1            
        result = sorted(wordFrequencies.keys(), key=(lambda k: wordFrequencies[k]), reverse = True)[:n]
        return result        
    
    
    def __simpleWordSplit(self, text):
        puncutation = '.,;:?!"/'
        for token in puncutation:
            text = text.replace(token, '')
        return text.split()