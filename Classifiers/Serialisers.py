import re
import json
from Classifiers.Bayesian import BayesianClassifier
from Classifiers.Features.Features import ClassificationFeature, WordClassificationFeature
from Classifiers.Classifier_Setup.BayesianClassifierSetup import SimpleSetup



def BayesianClassifierSerialise(classifier: BayesianClassifier):
    
    def jdefault(thing):
        if isinstance(thing, set):
            return list(thing)
        return thing.__dict__

    features = [x.serialise() for x in classifier.Features]

    jsonDictionary = {
        'classes': json.dumps(classifier.Classes, default = jdefault),
        'features': json.dumps(features, default = jdefault),
        'classprobabilities': json.dumps(classifier.ClassProbabilities, default = jdefault),
        'featureprobabilitiesgivenclass': json.dumps(classifier.FeatureProbabilitiesGivenClass, default = jdefault),    
        }

    jsonresult = json.dumps(jsonDictionary, default = jdefault)

    return jsonresult


def BayesianClassifierDeserialise(serialisedclassifier):

    jsonDictionary = json.loads(serialisedclassifier)

    dataDicationary = {
    'classes': set(json.loads(jsonDictionary['classes'])),
    'features': set(json.loads(jsonDictionary['features'])),
    'classprobabilities': json.loads(jsonDictionary['classprobabilities']),
    'featureprobabilitiesgivenclass': json.loads(jsonDictionary['featureprobabilitiesgivenclass']),
    }

    result = BayesianClassifier(SimpleSetup(dataDicationary))

    return result


def BayesianClassifierDeserialise_ftr(serialisedclassifier):
    from Serialisation.Simple import deserialise

    jsonDictionary = json.loads(serialisedclassifier)
    ftrs = json.loads(jsonDictionary['features'])
    features = {deserialise(x) for x in ftrs}

    dataDicationary = {
    'classes': set(json.loads(jsonDictionary['classes'])),
    'features': set(features),
    'classprobabilities': json.loads(jsonDictionary['classprobabilities']),
    'featureprobabilitiesgivenclass': json.loads(jsonDictionary['featureprobabilitiesgivenclass']),
    }

    result = BayesianClassifier(SimpleSetup(dataDicationary))

    return result





#def serialisable(cls):
#    class wrapper:
                
#        _registry = {}

#        def __init__(self, *args):
#            self._class = cls
#            self._serialisationargs = args
#            self._registry[cls.__name__] = cls             
#            self._wrapped = cls(*args)

#        def __getattr__(self, *args):
#            return getattr(self._wrapped, *args)

#        def serialise(self):
#            jsondictionary = {
#                'class': self._class.__name__,
#                'args': self._serialisationargs,
#                }

#            return json.dumps(jsondictionary)

#        @staticmethod
#        def deserialise(ser_str):
#            jsondictionary = json.loads(ser_str)

#            classname = jsondictionary['class']
#            makeargs = jsondictionary['args']
#            return wrapper._registry[classname](*makeargs)


#    return wrapper




