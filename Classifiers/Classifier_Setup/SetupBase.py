import abc

class ClassifierSetupProvider(abc.ABC):
       
    @abc.abstractproperty
    def Name(self):
        pass

    @abc.abstractproperty
    def Features(self):
        pass

    @abc.abstractproperty
    def GetClassProbabilities(self):
        pass
    
    @abc.abstractproperty
    def GetFeatureProbabilities(self):
        pass


