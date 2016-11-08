
from Helpers import TextHelpers
from Classifiers.Base import ClassifierBase
from Classifiers.TrainingData.TrainingBase import BinaryTrainingDataBase 

class BayesianClassifier(ClassifierBase):
    
    def __init__(self, trainingData: BinaryTrainingDataBase):
        self.__classes = trainingData.Classes
        self.__features = trainingData.Features
        self.__testData = trainingData.TestData
        self.__classProbabilities = trainingData.GetClassProbabilities()
        self.__featureProbabilitiesGivenClass = trainingData.GetFeatureProbabilities()
       
        

    def GetTestClassification(self):
        testClassifications = {}
        for text in self.__testData:
            testClassifications[text] = self.ClassifyText(text)
        return testClassifications


    def ClassifyText(self, text):
        probabilities = self.__getClassProbabilities(text)
        normaliser = sum(probabilities[z] for z in self.__classes)
        classification = max(
            [x for x in probabilities], 
            key = lambda z: probabilities[z]
            )
        result = (classification, probabilities[classification] / normaliser)
        return result


    def __getClassProbabilities(self, text):
        probabilities = {}
        for cl in self.__classes:
            classProbability = 1
            for feature in self.__features:
                occurrencesInText = TextHelpers.countoccurences(feature, text)

                if occurrencesInText > 0:
                    featureProbability = self.__featureProbabilitiesGivenClass[cl][feature] ** occurrencesInText
                else:
                    featureProbability = 1 - self.__featureProbabilitiesGivenClass[cl][feature]

                classProbability *= featureProbability
            
            probabilities[cl] = self.__classProbabilities[cl] * classProbability
        return probabilities



 

