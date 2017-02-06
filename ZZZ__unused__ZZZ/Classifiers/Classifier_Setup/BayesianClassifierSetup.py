from Classifiers.Classifier_Setup.SetupBase import ClassifierSetupProvider

class SimpleSetup(ClassifierSetupProvider):

    @property
    def Name(self):
        return self.__data['name']
    
    @property
    def Features(self):
        return self.__data['features']

    @property
    def TestData(self):
        return self.__data['testdata']


    def GetClassProbabilities(self):
        return self.__data['classprobabilities']
    

    def GetFeatureProbabilities(self):
        return self.__data['featureprobabilitiesgivenclass']

    def __init__(self, dataDictionary):
        self.__data = dataDictionary