from Helpers import TextHelpers
from Classifiers.Classifier_Setup.TrainingTextExperiment import TrainingTexts
from Classifiers.Classifier_Setup.SetupBase import SetupProvider


class ExperimentalTrainer(SetupProvider):

    @property
    def Classes(self):
        return [self.__name, self.__othername]
    
    @property
    def Features(self):
        return set.union(self.__extrinsicFeatures, self.__extractedFeatures)
    
    @property
    def ExtrinsicFeatures(self):
        return self.__extrinsicFeatures
        
    @property
    def TestData(self):
        return self.__testTexts    

    def GetTrainingTexts(self, cl):
        return self.__texts.get(cl, '')


    def GetClassProbabilities(self):
        result = {}
        for cl in self.Classes:
            result[cl] = self.__getClassProportion(cl)
        return result

    def __getClassProportion(self, cl):
        texts = self.GetTrainingTexts(cl)
        return len(texts) / (len(self.__texts[self.__name]) + len(self.__texts[self.__othername]))

    
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
                featureOccurences = TextHelpers.countoccurences(feature, classText)
                prob = (1 + featureOccurences) / totalDivisor
                featureProbabilitiesGivenClass[cl][feature] = prob
        return featureProbabilitiesGivenClass



    def __init__(self, keyword, trainingTexts: TrainingTexts):
        self.__trainingTexts = trainingTexts
        self.__stopwords = self.__trainingTexts.GetStopwords()
        self.__extrinsicFeatures = self.__trainingTexts.GetExtrinsicTerms()
                
        self.__name = keyword
        self.__othername = 'other'

        self.__texts = {
            self.__name: self.__trainingTexts.GetFeatureText(),
            self.__othername: self.__trainingTexts.GetNonFeatureText(),
            }

        self.__extractedFeatures = self.__extractFeatures()
        self.__features = set.union(self.__extrinsicFeatures, self.__extractedFeatures)

    
            

    def __extractFeatures(self):
        mostFrequentWordsInFeatureTexts = self.__getNMostFrequent(
            ' '.join([x
                      for x in self.__simpleWordSplit(self.__texts[self.__name])
                      if x.lower() not in self.__stopwords]),
            20)
        mostFrequentWordsOutsideFeatureTexts = self.__getNMostFrequent(
            ' '.join([x
                      for x in self.__simpleWordSplit(self.__texts[self.__othername])
                      if x.lower() not in self.__stopwords]), 
            1000)    
        extractedFeatures = {x for x in mostFrequentWordsInFeatureTexts if x not in mostFrequentWordsOutsideFeatureTexts}
        return extractedFeatures


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
