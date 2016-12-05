import unittest

class test_WordClassificationFeature(unittest.TestCase):
            
    def test_TrainingDataSetup(self):
        from Classifiers.Issue_Extraction.BayesianFeature import BayesianClassifier
        from Classifiers.Issue_Extraction.Features import WordClassificationFeature
        from Classifiers.Issue_Extraction.ClassifierSetup import TrainingDataSetup
        from Classifiers.Classifier_Setup import TrainingTexts 
        
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
        from Classifiers.Issue_Extraction.FeatureExtraction import WordClassificationFeature
        from Classifiers.Classifier_Setup.TrainingTexts import TrainingTexts

        trainingtexts = TrainingTexts('restitutio')
        extractor = WordExtractor(trainingtexts, 20)
        result = extractor.GetFeatures()

        test = [x.__repr__() for x in result]
        test1 = WordClassificationFeature('122')
        self.assertTrue(test1.__repr__() in test)
        

    def test_wordPairExtractor(self):
        from Classifiers.Issue_Extraction.FeatureExtraction import WordPairExtractor
        from Classifiers.Issue_Extraction.FeatureExtraction import WordClassificationFeature
        from Classifiers.Classifier_Setup.TrainingTexts import TrainingTexts

        trainingTexts = TrainingTexts('restitutio')
        extractor = WordPairExtractor(trainingTexts, 20)
        result = extractor.GetFeatures()

        test = [x.__repr__() for x in result]
        test1 = WordClassificationFeature(('Article','122'))
        self.assertTrue(test1.__repr__() in test)
        



    def test_substringExtractor(self):
        from Classifiers.Issue_Extraction.FeatureExtraction import SubstringExtractor
        from Classifiers.Classifier_Setup.TrainingTexts import TrainingTexts
        from Classifiers.Issue_Extraction.ClassifierSetup import TrainingDataSetup
        from Classifiers.Issue_Extraction.BayesianFeature import BayesianClassifier

        
        trainingTexts = TrainingTexts('restitutio')
        extractor = SubstringExtractor(trainingTexts, 10)
        features = extractor.GetFeatures()

        trainer = TrainingDataSetup('restitutio', features, trainingTexts)
        classifier = BayesianClassifier(trainer)
        result1 = classifier.ClassifyText("This short text talks of Article 122 EPC. It is about resitutio in integrum.")
        result2 = classifier.ClassifyText("Just some random stuff that could be about anything but is actually aobut nothing.")
        self.assertTrue(result1[0] == 'restitutio')
        self.assertTrue(result2[0] != 'restitutio')
 





