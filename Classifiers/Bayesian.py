
from Helpers import TextHelpers
from Classifiers.Base import ClassifierBase 

class BayesianClassifier(ClassifierBase):
    
    def __init__(self, trainingData):
        self.__trainingData = trainingData
        self.__initialiseVariables()        
        self.__trainClassifier()


    def __initialiseVariables(self):
        self.__classProbabilities = {}
        self.__featureProbabilitiesGivenClass = {}
        self.__testProbabilities = {}
        for cl in self.__trainingData.Classes:
            self.__testProbabilities[cl] = {}
        self.__testClassifications = {}



    def __trainClassifier(self):
        self.__setClassProbabilities()
        self.__setFeatureProbabilities()
        
    def __setClassProbabilities(self):
        for cl in self.__trainingData.Classes:
            self.__classProbabilities[cl] = self.__trainingData.GetClassProportion(cl)
            
    def __setFeatureProbabilities(self):  
        for cl in self.__trainingData.Classes:
            self.__featureProbabilitiesGivenClass[cl] = {}

            for feature in self.__trainingData.Features:

                aggregateText = ' '.join(self.__trainingData.GetTrainingTexts(cl))
                totalWordCount = TextHelpers.countwords(aggregateText)
                featureOccurences = TextHelpers.countoccurences(feature, aggregateText)
                prob = (1 + featureOccurences) / (totalWordCount + self.__trainingData.FeatureCount)
                self.__featureProbabilitiesGivenClass[cl][feature] = prob




    def ClassifyText(self, text):
        probabilities = {}
        for cl in self.__trainingData.Classes:
            classProbability = 1
            for feature in self.__trainingData.Features:
                occurrencesInText = TextHelpers.countoccurences(feature, text)

                if occurrencesInText > 0:
                    featureProbability = self.__featureProbabilitiesGivenClass[cl][feature] ** occurrencesInText
                else:
                    featureProbability = 1 - self.__featureProbabilitiesGivenClass[cl][feature]

                classProbability *= featureProbability

            probabilities[cl] = self.__classProbabilities[cl] * classProbability

        normaliser = sum(probabilities[z] for z in self.__trainingData.Classes)
        classification = max(
            [x for x in probabilities], 
            key = lambda z: probabilities[z]
            )
        result = (classification, probabilities[classification] / normaliser)

        return result


    def GetTestClassification(self):
        testClassifications = {}
        for text in self.__trainingData.TestData:
            testClassifications[text] = self.ClassifyText(text)
        return testClassifications




 

