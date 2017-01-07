from DecisionAnalyser.ViewModels.Base import VMBase

from app.DBProxy import DecisionModelProxy
from DecisionAnalyser.models import ClassifierSerialisationModel


def makeAnalyser():
    from Classifiers.Bayesian import BayesianClassifier
    
    de_classifier = BayesianClassifier.MakeClassifier(
        'restitutio', 
        ['restitutio', 'integrum'], 
        [('122', 'EPC')]
        )

    en_classifier = BayesianClassifier.MakeClassifier(
        'restitutio', 
        ['restitutio', 'integrum'], 
        [('122', 'EPC'), ('due', 'care')]
        )
    
    fr_classifier = BayesianClassifier.MakeClassifier(
        'restitutio', 
        ['restitutio', 'integrum'], 
        [('122', 'EPC')]
        )

    from DecisionAnalyser.EPOAnalyser.TextAnalyser import Analyser
    analyser = Analyser(de_classifier = de_classifier, en_classifier = en_classifier, fr_classifier = fr_classifier)
    return analyser



class  TryoutViewModel(VMBase):
    
    def __init__(self, decisions):
        super(TryoutViewModel, self).__init__()

        analyser = makeAnalyser()
        decision = decisions[0].first()
        text = analyser.Analyse_Decision(decision)
        
        self.Context.update({
                'decision': decision,
                'facts': [(x, self.threshhold(y)) for (x, y) in text['Facts']],
                'reasons': [(x, self.threshhold(y)) for (x, y) in text['Reasons']],
                'order': [(x, self.threshhold(y)) for (x, y) in text['Order']],
                })


    def threshhold(self, probability):
        if probability > 0.8:
            return "high"
        if probability > 0.6:
            return "medium"
        if probability > 0.4:
            return "low"
        return "none"



