from app.DBProxy import DecisionModelProxy
from Classifiers.Bayesian import BayesianClassifier
from Classifiers.Classifier_Setup.TrainingTextBase import TrainingTextProvider
from Classifiers.Classifier_Setup import Texts


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
        self.__decisions = self.__getDecisionsWithKeyordinKeywordsfield()
        self.__featureTexts, self.__otherTexts = self.__getRelevantPargaphsFromDecisions()


    def __getDecisionsWithKeyordinKeywordsfield(self): 
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