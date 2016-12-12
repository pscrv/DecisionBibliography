from app.DBProxy import DecisionModelProxy
from Helpers import TextHelpers
from Classifiers.TrainingTexts import Texts
from Classifiers.Bayesian import BayesianClassifier
from Classifiers.TrainingTexts.TrainingTextBase import TrainingTextProvider



class BasicDBTextFinder(TrainingTextProvider):

    def GetFeatureText(self):
        return self.__featureTexts
    
    def GetNonFeatureText(self):
        return self.__otherTexts

    def GetStopwords(self):
        return Texts.GetStopwords()

    def GetExtrinsicTerms(self):
        return self.__baseTrainer.ExtrinsicFeatures

    
    
    def GetFeatureTextWordCount(self):
        return TextHelpers.countwords(self.__featureTexts)

    def GetReducedFeatureText(self):
        return self.__reducedFeatureTexts

    
    def GetNonFeatureTextWordCount(self):
        return TextHelpers.countwords(self.__otherTexts)    
    
    def GetReducedNonFeatureText(self):
        return self.__reducedOtherTexts




    def __init__(self, keyword,):
        self.__paragarphMargin = 3
        self.__keyword = keyword
        self.__decisions = self.__getDecisionsWithKeyordInKeywordsField()
        self.__featureTexts, self.__otherTexts = self.__getRelevantPargaphsFromDecisions()

        self.__stopwords = Texts.GetStopwords()
        self.__reducedFeatureTexts = TextHelpers.removeWords(self.__featureTexts, self.__stopwords)
        self.__reducedOtherTexts = TextHelpers.removeWords(self.__otherTexts, self.__stopwords)

    def __getDecisionsWithKeyordInKeywordsField(self): 
        decisions = DecisionModelProxy.GetBibliographyFiltered(Keywords__contains = self.__keyword)
        return [x for x in decisions if x.DecisionLanguage == 'EN']

    def __getRelevantPargaphsFromDecisions(self):
        featureTexts = []
        otherTexts = []
        for decision in self.__decisions:
            decisionText = DecisionModelProxy.GetTextFromDecision(decision)
            if decisionText:
                reasonsParagraphs = decisionText.Reasons.split('\n\n')

                paragraphsToRemove = set()
                numberOfParagraphs = len(reasonsParagraphs)
                for index in range(0, numberOfParagraphs):
                    if self.__keyword in reasonsParagraphs[index]:
                        featureTexts.append(reasonsParagraphs[index])
                        minIndex = max(0, index - self.__paragarphMargin)
                        maxIndex = min(numberOfParagraphs, index + self.__paragarphMargin + 1)
                        for removalIndex in range(minIndex, maxIndex):
                            paragraphsToRemove.add(removalIndex)
                otherTexts += [reasonsParagraphs[index] for index in range(0, numberOfParagraphs) 
                               if index not in paragraphsToRemove]


        return ''.join(featureTexts), ' '.join(otherTexts)




class DecisionTextFinder(TrainingTextProvider):

    def GetFeatureText(self):
        return self.__featureTexts
    
    def GetNonFeatureText(self):
        return self.__otherTexts

    def GetStopwords(self):
        return Texts.GetStopwords()

    def GetExtrinsicTerms(self):
        return self.__baseTrainer.ExtrinsicFeatures


    def __init__(self, keyword, baseTrainer):
        self.__keyword = keyword
        self.__baseTrainer = baseTrainer
        self.__featureTexts = []
        self.__otherTexts = []
        self.__decisions = None
        self.__baseclassifier = BayesianClassifier(self.__baseTrainer)
        self.__decisions = self.__getDecisionsWithKeyordInKeywordsField()
        self.__featureTexts, self.__otherTexts = self.__getRelevantPargaphsFromDecisions()


    def __getDecisionsWithKeyordInKeywordsField(self): 
        return DecisionModelProxy.GetBibliographyFiltered(Keywords__contains = self.__keyword)

    def __getRelevantPargaphsFromDecisions(self):
        featureTexts = []
        otherTexts = []
        for decision in self.__decisions:
            decisionText = DecisionModelProxy.GetTextFromDecision(decision)
            if decisionText:
                reasonsParagraphs = decisionText.Reasons.split('\n\n')

                for paragraph in reasonsParagraphs:
                    classification, probability = self.__baseclassifier.ClassifyText(paragraph)
                    if classification == self.__keyword and probability > 0.70:
                        featureTexts.append(paragraph)
                    if classification != self.__keyword and probability > 0.80:
                        otherTexts.append(paragraph)

        return ''.join(featureTexts), ' '.join(otherTexts)