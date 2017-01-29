from DecisionAnalyser.ViewModels.Base import VMBase

class AnalysedDecisionViewModel(VMBase):
    
    def __init__(self, decision, analysername):
        super(AnalysedDecisionViewModel, self).__init__()

        analyser = makeAnalyser(analysername)
        text = analyser.Analyse_Decision(decision)
        
        self.Context.update({
                'decision': decision,
                'facts': [(x, threshhold(y)) for (x, y) in text['Facts']],
                'reasons': [(x, threshhold(y)) for (x, y) in text['Reasons']],
                'order': [(x, threshhold(y)) for (x, y) in text['Order']],
                'analysername': analyser.Name,
                })
        


def makeAnalyser(name):
    from Classifiers.Bayesian import BayesianClassifier
    from DecisionAnalyser.EPOAnalyser.TextAnalyser import Analyser, NullAnalyser

    setupdata = analyserSetupData.get(name, None)
    if not setupdata:
        return NullAnalyser();

    de_classifier = BayesianClassifier.MakeClassifier(*setupdata['de'])
    en_classifier = BayesianClassifier.MakeClassifier(*setupdata['en'])
    fr_classifier = BayesianClassifier.MakeClassifier(*setupdata['fr'])


    analyser = Analyser(de_classifier = de_classifier, en_classifier = en_classifier, fr_classifier = fr_classifier)
    return analyser



analyserSetupData = {}
analyserSetupData['restitutio'] = {
    'de': ('restitutio', ['resititutio', 'integrum' ], [('122', 'EPC')]),
    'en': ('restitutio', ['restitutio', 'integrum'],[('122', 'EPC'), ('due', 'care')]),
    'fr': ('restitutio', ['restitutio', 'integrum'], [('122', 'EPC')]),
    }
analyserSetupData['added subject-matter'] = {
    'de': ('added subject-matter', ['erweitert', 'erweiterung'], [('123(2)', 'EPC'), ('ursprunglich', 'eingereicht'), ('urspruenglich', 'eingereicht')]),
    'en': ('added subject-matter', ['extends', 'extended'], [('123(2)', 'EPC'), ('as', 'filed')]),
    'fr': ('added subject-matter', ['etend', 'etendu'], [('123(2)', 'EPC'), ('au', 'dela')]),
    }


def threshhold(probability):
    if probability > 0.8:
        return "high"
    if probability > 0.6:
        return "medium"
    if probability > 0.4:
        return "low"
    return "none"

