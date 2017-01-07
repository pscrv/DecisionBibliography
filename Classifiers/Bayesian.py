from Helpers import TextHelpers
from Classifiers.Base import ClassifierBase
from Classifiers.Classifier_Setup.SetupProvider import ClassifierSetupProvider


class BayesianClassifier(ClassifierBase):

    @classmethod
    def MakeClassifier(cls, trainingtextname, words, wordpairs):
        words_ok = all(isinstance(x, str) for x in words)
        if not words_ok:
            raise TypeError('parameter "words" is not an iterable of strings')

        pairs_ok = all(isinstance(x, str) and isinstance(y, str)
                       for (x, y) in wordpairs)
        if not pairs_ok:
            raise TypeError('parameter "wordpairs" is not an iterable of (string, string)')


        from Classifiers.Classifier_Setup.SetupProvider import TrainingDataSetup
        from Classifiers.Features.Features import WordClassificationFeature, StringInWordPairClassificationFeature
        from Classifiers.TrainingTexts.TrainingTexts import TrainingTexts
        features = ([WordClassificationFeature(x) for x in words] 
                    + [StringInWordPairClassificationFeature(x, y) for (x, y) in wordpairs])   
        trainingtexts = TrainingTexts(trainingtextname)
        trainer = TrainingDataSetup(trainingtextname, features, trainingtexts)
        classifier = BayesianClassifier(trainer)
        return classifier

    @property
    def Name(self):
        return self.__name

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


    
    def __init__(self, setupdata: ClassifierSetupProvider):
        self.__name = setupdata.Name
        self.__classes = [self.__name, 'other']
        self.__features = setupdata.Features
        self.__classProbabilities = setupdata.GetClassProbabilities()
        self.__featureProbabilitiesGivenClass = setupdata.GetFeatureProbabilities()
       
        



    def ClassifyText(self, text):
        probabilities = self.__getClassProbabilities(text)
        normaliser = sum(probabilities[z] for z in self.__classes)
        result = probabilities[self.__name] / normaliser
        return result


    def __getClassProbabilities(self, text):
        probabilities = {}
        for cl in self.__classes:
            classProbability = 1
            for feature in self.__features:
                occurrencesInText = feature.CountOccurrences(text)

                if occurrencesInText > 0:
                    featureProbability = self.__featureProbabilitiesGivenClass[cl][feature.Name] ** occurrencesInText
                else:
                    featureProbability = 1 - self.__featureProbabilitiesGivenClass[cl][feature.Name]

                classProbability *= featureProbability
            
            probabilities[cl] = self.__classProbabilities[cl] * classProbability
        return probabilities



 

