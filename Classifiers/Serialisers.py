import re
import json
from Classifiers.Bayesian import BayesianClassifier
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




