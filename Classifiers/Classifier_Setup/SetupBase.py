import abc

class SetupProvider(abc.ABC):
   
    @abc.abstractproperty
    def Classes(self):
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