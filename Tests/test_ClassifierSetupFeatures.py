import unittest

class test_WordClassificationFeature(unittest.TestCase):
            
    def test_TrainingDataSetup(self):
        from Classifiers.Issue_Extraction.BayesianFeature import BayesianClassifier
        from Classifiers.Issue_Extraction.Features import WordClassificationFeature
        from Classifiers.Classifier_Setup import TrainingTexts 
        from Classifiers.Issue_Extraction.ClassifierSetup import TrainingDataSetup
        
        featureStrings = ['122', 'restitutio', 'integrum', 'due', 'care',]
        features = [WordClassificationFeature(x) for x in featureStrings]
        texts = TrainingTexts.TrainingTexts('restitutio')
        trainer = TrainingDataSetup('restitutio', features, texts)
        classifier = BayesianClassifier(trainer)
        result1 = classifier.ClassifyText('Text about restitutio (Article 122 EPC).')
        result2 = classifier.ClassifyText('Some stupid text all about nothing.')
        self.assertEqual(result1[0], 'restitutio')
        self.assertEqual(result2[0], 'other')
        
            
    def test_StringInWordPairClassificationFeature(self):
        from Classifiers.Issue_Extraction.BayesianFeature import BayesianClassifier
        from Classifiers.Issue_Extraction.Features import WordClassificationFeature, StringInWordPairClassificationFeature
        from Classifiers.Classifier_Setup import TrainingTexts 
        from Classifiers.Issue_Extraction.ClassifierSetup import TrainingDataSetup
        
        featureStrings = ['restitutio', 'integrum',]
        featureStringPairs = [('122', 'EPC'), ('Art', '122'), ('due', 'care')]
        features = ([WordClassificationFeature(x) for x in featureStrings] 
                    + [StringInWordPairClassificationFeature(x, y) for (x, y) in featureStringPairs])
        texts = TrainingTexts.TrainingTexts('restitutio')
        trainer = TrainingDataSetup('restitutio', features, texts)
        classifier = BayesianClassifier(trainer)
        result1 = classifier.ClassifyText('Text about restitutio (Article 122 EPC).')
        result2 = classifier.ClassifyText('Some stupid text all about nothing.')
        self.assertEqual(result1[0], 'restitutio')
        self.assertEqual(result2[0], 'other')

