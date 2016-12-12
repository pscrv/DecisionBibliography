import django
from django.test import TestCase


class test_TextFromDB(TestCase):
        
    @classmethod
    def setUpClass(cls):    
        super(test_TextFromDB, cls).setUpClass()
        django.setup()
        

    def test_restitutioFromDB(self):
        from Classifiers.Bayesian import BayesianClassifier
        from Classifiers.Classifier_Setup.SetupProvider import TrainingDataSetup
        from Classifiers.Features.FeatureExtraction import WordPairExtractor, WordExtractor
        from Classifiers.TrainingTexts.TextsfFromDB import BasicDBTextFinder
                        
        trainingTexts = BasicDBTextFinder('restitutio')
        pair_extractor = WordPairExtractor(trainingTexts, 5)
        pairs = pair_extractor.GetFeatures()
        word_extractor = WordExtractor(trainingTexts, 5)
        words = word_extractor.GetFeatures()
        features = pairs + words
        trainer = TrainingDataSetup('restitutio', features, trainingTexts)
        classifier = BayesianClassifier(trainer)
        
        test1 = """This paragraph is about restitutio in integrum. It refers to Article 122 EPC:"""
        test2 = """ Some random paragraph that talks, if of anything at all, only about itself. It has nothing to do with anything."""
        result1 = classifier.ClassifyText(test1)
        result2 = classifier.ClassifyText(test2)
        self.assertEqual(result1[0], 'restitutio')
        self.assertEqual(result2[0], 'other')

