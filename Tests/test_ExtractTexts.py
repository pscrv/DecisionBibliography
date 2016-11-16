import datetime
import django
from django.test import TestCase


class test_Extraction(TestCase):
            
    @classmethod
    def setUpClass(cls):    
        super(test_Extraction, cls).setUpClass()
        django.setup()

    def test_ExperimentalRestitutioExtraction(self):
        from Classifiers.Classifier_Setup.TrainingTextExperiment import TrainingTexts
        from Classifiers.Classifier_Setup.TrainerExperiment import ExperimentalTrainer
        from Classifiers.Bayesian import BayesianClassifier

        extrinsicIndicators = {'122', 'restituio', 'integrum', 'all', 'due', 'care'}
        texts = TrainingTexts('restitutio', extrinsicIndicators)
        trainer = ExperimentalTrainer('restitutio', texts)
        classifier = BayesianClassifier(trainer)
        
        test1 = """This paragraph is about restitutio in integrum. It refers to Article 122 EPC:"""
        test2 = """ Some random paragraph that talks, if of anything at all, only about itself."""

        result1 = classifier.ClassifyText(test1)
        result2 = classifier.ClassifyText(test2)
        self.assertEqual(result1[0], 'restitutio')
        self.assertEqual(result2[0], 'other')


    def test_RestitutioTextProvider(self):
        from Classifiers.Classifier_Setup.TrainingTextExperiment import TrainingTexts
        from Classifiers.Classifier_Setup.TrainerExperiment import ExperimentalTrainer
        from Classifiers.Bayesian import BayesianClassifier
        from Classifiers.Issue_Extraction.TextProvider import DecisionTextFinder
        
        extrinsicIndicators = {'122', 'restitutio', 'integrum', 'due', 'care'}
        baseTexts = TrainingTexts('restitutio', extrinsicIndicators)
        baseTrainer = ExperimentalTrainer('restitutio', baseTexts)

        texts = DecisionTextFinder('restitutio', baseTrainer)
        trainer = ExperimentalTrainer('restitutio', texts)
        classifier = BayesianClassifier(trainer)

        test1 = """This paragraph is about restitutio in integrum. It refers to Article 122 EPC:"""
        test2 = """ Some random paragraph that talks, if of anything at all, only about itself."""

        result1 = classifier.ClassifyText(test1)
        result2 = classifier.ClassifyText(test2)
        self.assertEqual(result1[0], 'restitutio')
        self.assertEqual(result2[0], 'other')


    def test_MathematicalMethodTextProvider(self):
        from Classifiers.Classifier_Setup.TrainingTextExperiment import TrainingTexts
        from Classifiers.Classifier_Setup.TrainerExperiment import ExperimentalTrainer
        from Classifiers.Bayesian import BayesianClassifier
        from Classifiers.Issue_Extraction.TextProvider import DecisionTextFinder
        
        extrinsicIndicators = {'52(2)', '52(3)', 'mathematical', 'method', 'exclude',}
        baseTexts = TrainingTexts('mathematicalmethod', extrinsicIndicators)
        baseTrainer = ExperimentalTrainer('mathematicalmethod', baseTexts)

        texts = DecisionTextFinder('mathematicalmethod', baseTrainer)
        trainer = ExperimentalTrainer('mathematicalmethod', texts)
        classifier = BayesianClassifier(trainer)

        test1 = """This paragraph is about mathematical methods. It refers to Article 52(2) EPC:"""
        test2 = """ Some random paragraph that talks, if of anything at all, only about itself."""

        result1 = classifier.ClassifyText(test1)
        result2 = classifier.ClassifyText(test2)
        self.assertEqual(result1[0], 'mathematicalmethod')
        self.assertEqual(result2[0], 'other')


