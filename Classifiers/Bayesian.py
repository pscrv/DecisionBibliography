from Helpers import TextHelpers
from Classifiers.Base import ClassifierBase
from Classifiers.Classifier_Setup.SetupBase import SetupProvider 


class BayesianClassifier(ClassifierBase):

    @property
    def Classes(self):
        return {x for x in self.__classes}

    @property
    def Features(self):
        return {x for x in self.__features}
    
    @property
    def ClassProbabilities(self):
        return {x:y for x,y in self.__classProbabilities.items()}
        
    @property
    def FeatureProbabilitiesGivenClass(self):
        return {x:y for x,y in self.__featureProbabilitiesGivenClass.items()}

   


    
    def __init__(self, setupdata: SetupProvider):
        self.__classes = setupdata.Classes
        self.__features = setupdata.Features
        self.__classProbabilities = setupdata.GetClassProbabilities()
        self.__featureProbabilitiesGivenClass = setupdata.GetFeatureProbabilities()
       
        



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



 

