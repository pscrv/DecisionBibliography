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


    def test_wordExtractor(self):
        from Classifiers.Issue_Extraction.FeatureExtraction import WordExtractor
        from Classifiers.Classifier_Setup import Texts
        from Classifiers.Issue_Extraction.FeatureExtraction import WordClassificationFeature

        goodtext = Texts.GetText('restitutio')
        badtext = Texts.GetText('-restitutio')
        stopwords = Texts.GetStopwords()        
        extractor = WordExtractor(goodtext, badtext, stopwords, 20)
        result = extractor.GetFeatures()

        test = [x.__repr__() for x in result]


        test1 = WordClassificationFeature('122')
        self.assertTrue(test1.__repr__() in test)
        

    def test_substringExtractor(self):
        from Classifiers.Issue_Extraction.FeatureExtraction import SubstringExtractor
        from Classifiers.Classifier_Setup import Texts
        from Classifiers.Classifier_Setup.TrainingTexts import TrainingTexts
        from Classifiers.Issue_Extraction.FeatureExtraction import StringClassificationFeature
        from Classifiers.Issue_Extraction.ClassifierSetup import TrainingDataSetup
        from Classifiers.Issue_Extraction.BayesianFeature import BayesianClassifier

        goodtext = Texts.GetText('restitutio')
        badtext = Texts.GetText('-restitutio')
        stopwords = Texts.GetStopwords()        
        extractor = SubstringExtractor(goodtext, badtext, stopwords, 10)
        features = extractor.GetFeatures()

        trainingtexts = TrainingTexts('restitutio')
        trainer = TrainingDataSetup('restitutio', features, trainingtexts)
        classifier = BayesianClassifier(trainer)
        result1 = classifier.ClassifyText("This short text talks of Article 122 EPC. It is about resitutio in integrum.")
        result2 = classifier.ClassifyText("Just some random stuff that could be about anything but is actually aobut nothing.")
        self.assertTrue(result1[0] == 'restitutio')
        self.assertTrue(result2[0] != 'restitutio')
 





