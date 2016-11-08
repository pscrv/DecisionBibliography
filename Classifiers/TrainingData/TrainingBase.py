import abc
from Helpers import TextHelpers

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
        return self._texts.get(cl, '')

    def GetClassProportion(self, cl):
        texts = self.GetTrainingTexts(cl)
        return len(texts) / (len(self._texts[self._name]) + len(self._texts['other']))

    def GetClassProbabilities(self):
        result = {}
        for cl in self._classes:
            result[cl] = self.GetClassProportion(cl)
        return result
    

    def GetFeatureProbabilities(self):
        featureProbabilitiesGivenClass = {}
        for cl in self._classes:
            featureProbabilitiesGivenClass[cl] = {}
            classText = self.GetTrainingTexts(cl)
            totalWordCount = TextHelpers.countwords(classText)

            for feature in self.Features:
                featureOccurences = TextHelpers.countoccurences(feature, classText)
                prob = (1 + featureOccurences) / (totalWordCount + len(self._features))
                featureProbabilitiesGivenClass[cl][feature] = prob
        return featureProbabilitiesGivenClass


    @property
    def Classes(self):
        return self._classes
    
    @property
    def Features(self):
        return self._features
        
    @property
    def TestData(self):
        return self._testTexts
    
    




class BinaryTrainingDate_WithExtraction_Base(BinaryTrainingDataBase):

    @abc.abstractmethod
    def _extractFeatures():
        pass
    
    @property
    def Features(self):
        if self._features == []:
            self._extractFeatures()
        return self._features




    def __init__(self, name):
        super(BinaryTrainingDate_WithExtraction_Base, self).__init__(name)
        
        self._extrinsicFeatures = {}
        self.__extractedFeatures = {}
                


    def _extractFeatures(self):
        self.__extractFeaturesFromTexts()
        self._features = set.union(self._extrinsicFeatures, self.__extractedFeatures)
        

    def __extractFeaturesFromTexts(self):
        stopwords = {
            'a', 'an', 'the', 'this', 'that', 'those', 'these',
            'and', 'but',
            'as', 'after', 'before', 'in', 'at', 'on', 'over', 'under', 'to', 'with', 'without', 'of', 'for', 'from', 'about',
            'I', 'you', 'he', 'she', 'it', 'we', 'they',
            'am', 'are', 'is', 'was', 'were', 'be',
            'not',
            }
        
        fullTexts = {
            'feature' : self._texts[self._name],
            'other' : self._texts['other'],
            }

        reducedTexts = {
            'feature' : ' '.join([x for x in self.__simpleWordSplit(fullTexts['feature']) if x.lower() not in stopwords]),
            'other' : ' '.join([x for x in self.__simpleWordSplit(fullTexts['other']) if x.lower() not in stopwords]),
            }

        mostFrequent= {
            'feature' : self.__getNMostFrequent(reducedTexts['feature'], 10),
            'other' : self.__getNMostFrequent(reducedTexts['other'], 50)
            }

        self.__extractedFeatures = {x for x in mostFrequent['feature'] if x not in mostFrequent['other']}




    def __getNMostFrequent(self, text, n = 10):
        if not text:
            return None
        
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