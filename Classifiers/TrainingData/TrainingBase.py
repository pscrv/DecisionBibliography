import abc
from Helpers import TextHelpers
from Classifiers.TrainingData import Texts

class BinaryTrainingDataBase(abc.ABC):

    def __init__(self, keyword):
        self._extrinsicFeatures = set()
        self._extractedFeatures = set()
        self._testTexts = []
                
        self._name = keyword
        self._othername = 'other'
        self._texts = {
            self._name: Texts.GetText(keyword),
            self._othername: Texts.GetText('-' + keyword)
            }



    @property
    def Classes(self):
        return [self._name, self._othername]
    
    @property
    def Features(self):
        return set.union(self._extrinsicFeatures, self._extractedFeatures)
        
    @property
    def TestData(self):
        return self._testTexts
    

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
                featureOccurences = TextHelpers.countoccurences(feature, classText)
                prob = (1 + featureOccurences) / totalDivisor
                featureProbabilitiesGivenClass[cl][feature] = prob
        return featureProbabilitiesGivenClass

    




class BinaryTrainingDate_WithExtraction_Base(BinaryTrainingDataBase):

    @abc.abstractmethod
    def _extractFeatures():
        pass
    
    @property
    def Features(self):
        if not self._extractedFeatures:
            self._extractFeatures()
        return super(BinaryTrainingDate_WithExtraction_Base, self).Features




    #def __init__(self, keyword):
    #    super(BinaryTrainingDate_WithExtraction_Base, self).__init__(keyword)
        #self._extrinsicFeatures = set()
        #self._extractedFeatures = set()
                


    def _extractFeatures(self):
        self.__extractFeaturesFromTexts()
        self._features = set.union(self._extrinsicFeatures, self._extractedFeatures)
        

    def __extractFeaturesFromTexts(self):
        stopwords = Texts.GetStopwords()        
        fullTexts = {
            'feature' : self._texts[self._name],
            'other' : self._texts[self._othername],
            }
        reducedTexts = {
            'feature' : ' '.join([x for x in self.__simpleWordSplit(fullTexts['feature']) if x.lower() not in stopwords]),
            'other' : ' '.join([x for x in self.__simpleWordSplit(fullTexts['other']) if x.lower() not in stopwords]),
            }
        mostFrequent= {
            'feature' : self.__getNMostFrequent(reducedTexts['feature'], 10),
            'other' : self.__getNMostFrequent(reducedTexts['other'], 50)
            }
        self._extractedFeatures = {x for x in mostFrequent['feature'] if x not in mostFrequent['other']}
        

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
        puncutation = ".,;:?!'/"
        for token in puncutation:
            text = text.replace(token, '')
        return text.split()