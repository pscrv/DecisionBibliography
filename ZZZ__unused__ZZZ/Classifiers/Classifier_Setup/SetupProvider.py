from Classifiers.Classifier_Setup.SetupBase import ClassifierSetupProvider
from Classifiers.Features.Features import ClassificationFeature
from Helpers import TextHelpers

class TrainingDataSetup(ClassifierSetupProvider):

    def __init__(self, name, features, trainingTexts):
        self._trainingTexts = trainingTexts
        self._stopwords = self._trainingTexts.GetStopwords()
        self._features = set(features)

        self._name = name
        self._othername = 'other'

        self._texts = {
            self._name: self._trainingTexts.GetFeatureText(),
            self._othername: self._trainingTexts.GetNonFeatureText(),
            }
    

    @property
    def Classes(self):
        return [self._name, self._othername]
    


    @property 
    def Name(self):
        return self._name
    @property
    def Features(self):
        return self._features
   


    def GetClassProbabilities(self):
        result = {}
        for cl in self.Classes:
            result[cl] = self.__getClassProportion(cl)
        return result
    
    def GetFeatureProbabilities(self):
        featuresCount = len(self._features)
        featureProbabilitiesGivenClass = {}
        for cl in self.Classes:
            featureProbabilitiesGivenClass[cl] = {}
            classText = self.__getTrainingTexts(cl)
            totalWordCount = TextHelpers.countwords(classText)
            totalDivisor = totalWordCount + featuresCount

            for feature in self._features:
                featureOccurences = feature.CountOccurrences(classText)
                prob = (1 + featureOccurences) / totalDivisor
                featureProbabilitiesGivenClass[cl][feature.Name] = prob
        return featureProbabilitiesGivenClass



    def __getTrainingTexts(self, cl):
        return self._texts.get(cl, '')

    def __getClassProportion(self, cl):
        texts = self.__getTrainingTexts(cl)
        featureTextsLength = len(self._texts[self._name])
        nonFeatureTextsLength = len(self._texts[self. _othername])
        return len(texts) / (featureTextsLength + nonFeatureTextsLength)