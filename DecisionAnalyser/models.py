from django.db import models
from Classifiers import Bayesian
from Classifiers.Serialisers import BayesianClassifierSerialise, BayesianClassifierDeserialise


class ClassifierSerialisationManager(models.Manager):
    
    def SaveBayesianClassifier(self, name: str, classifier: Bayesian):
        serialisedClassifier =  BayesianClassifierSerialise(classifier)
        inDB = self.filter(Name = name)
        if inDB:
            model = inDB.first()
            model.Serialised = serialisedClassifier
        else:
            model = ClassifierSerialisationModel(Name = name, Serialised = serialisedClassifier)
        model.save()


    def RetrieveBayesianclassifier(self, name: str):
        inDB = self.filter(Name = name)
        if not inDB:
            return None

        model = inDB.first()
        return BayesianClassifierDeserialise(model.Serialised)





class ClassifierSerialisationModel(models.Model):
    objects = ClassifierSerialisationManager()
    
    Name = models.CharField(max_length = 50, default = "")
    Serialised = models.TextField()
   
    def __str__(self):
        return self.Name