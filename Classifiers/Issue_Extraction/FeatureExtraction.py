import abc
from Helpers import TextHelpers
from Classifiers.Issue_Extraction.Features import WordClassificationFeature, StringClassificationFeature

class FeatureExtractor(abc.ABC):

    @abc.abstractmethod
    def GetFeatures(self):
        pass


    def __init__(self, goodtext, badtext, stopwords, featurenumber):
        self._goodText = goodtext
        self._badText = badtext
        self._stopWords = stopwords
        self._featureNumber = featurenumber
        self._features = None
        self._goodWordCount = TextHelpers.countwords(self._goodText)
        self._badWordCount = TextHelpers.countwords(self._badText)




class WordExtractor(FeatureExtractor):

    def GetFeatures(self):
        if not self._features:
            self._features = self._extractFeatures()
        return self._features
    

    def _extractFeatures(self):
        goodWordFrequencies = { word : TextHelpers.countwordoccurences(word, self._goodText) / self._goodWordCount
                               for word in {x for x in TextHelpers.getwords(self._goodText) if x not in self._stopWords}
                               } 

        badWordFrequencies = { word : TextHelpers.countwordoccurences(word, self._badText) / self._badWordCount
                               for word in {x for x in TextHelpers.getwords(self._badText) if x not in self._stopWords}
                               }
        
        keptWords = sorted(
            goodWordFrequencies.keys(), 
            key=(lambda k: goodWordFrequencies[k] - badWordFrequencies.get(k, 0)), 
            reverse = True
            )[:self._featureNumber]

        result = [WordClassificationFeature(x) for x in keptWords]

        return result

 
        
class SubstringExtractor(FeatureExtractor):

    _minlength = 5
    
    def GetFeatures(self):
        if not self._features:
            self._features = self._extractFeatures()
        return self._features



    def _extractFeatures(self):
        goodWords = { word for word in TextHelpers.getwords(self._goodText) if word not in self._stopWords }
        shortGoodWords = { word for word in goodWords if len(word) <= self._minlength }
        shortWordGains = { x : self._stringGain(x) for x in shortGoodWords}
        longGoodWords = set.difference(goodWords, shortGoodWords)        
        stringGains = self._getSubstringGains(longGoodWords)            
        allGains = {**stringGains, **shortWordGains}

        keptWords = sorted(
            allGains.keys(), 
            key=(lambda k: allGains[k]), 
            reverse = True
            )[:self._featureNumber]

        result = [StringClassificationFeature(x) for x in keptWords if allGains[x] > 1.0]

        return result


    def _getSubstringGains(self, longGoodWords):
        stringGains = {
            bestSubstring : gain 
            for (bestSubstring, gain) in 
                (self._bestSubstringAndGain(word) for word in longGoodWords)
            }
        return stringGains


    def _bestSubstringAndGain(self, word):
        wordGain = self._stringGain(word)
        maxGainForLength = 0
        maxGainPosition = 0
        for length in range(len(word) - 1, self._minlength - 1, -1):
            maxGainForLength, maxGainPosition = self._maxGainAndPosition(word, length)
            if maxGainForLength < wordGain:
                break
        bestSubstring = word[maxGainPosition:length]
        return bestSubstring, wordGain




    def _maxGainAndPosition(self, word, length):
        maxGain = 0
        for start in range(0, len(word) - length + 1):
            gain = self._stringGain(word[start:length])
            if gain >= maxGain:
                maxGain = gain
                maxPosition = start
        return maxGain, maxPosition



    def _stringGain(self, string):
        goodFrequency = TextHelpers.countstringoccurencesinword(string, self._goodText)
        badFrequency = TextHelpers.countstringoccurencesinword(string, self._badText)
        if badFrequency == 0:
            badFrequency = 0.1 / self._badWordCount
        gain = goodFrequency / badFrequency
        return gain




        