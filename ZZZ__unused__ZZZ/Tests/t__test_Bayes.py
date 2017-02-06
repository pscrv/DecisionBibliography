import unittest

from Classifiers.Bayesian import BayesianClassifier
from Classifiers.Classifier_Setup.SetupProvider import TrainingDataSetup
from Classifiers.Features.FeatureExtraction import WordPairExtractor, WordExtractor, SubstringExtractor
from Classifiers.TrainingTexts.TrainingTexts import TrainingTexts

class test_Bayes(unittest.TestCase):
            

    def test_restitutioClassifier(self):
                
        trainingTexts = TrainingTexts('restitutio')
        pair_extractor = WordPairExtractor(trainingTexts, 20)
        pairs = pair_extractor.GetFeatures()
        word_extractor = WordExtractor(trainingTexts, 10)
        words = word_extractor.GetFeatures()
        features = pairs + words
        trainer = TrainingDataSetup('restitutio', features, trainingTexts)
        classifier = BayesianClassifier(trainer)
        
        test1 = """This paragraph is about restitutio in integrum. It refers to Article 122 EPC:"""
        test2 = """ Some random paragraph that talks, if of anything at all, only about itself."""
        result1 = classifier.ClassifyText(test1)
        result2 = classifier.ClassifyText(test2)
        self.assertGreater(result1, 0.5)
        self.assertLess(result2, 0.5)

        

    def test_restitutioClassifierLongerText(self):
                
        trainingTexts = TrainingTexts('restitutio')
        pair_extractor = WordPairExtractor(trainingTexts, 0)
        pairs = pair_extractor.GetFeatures()
        word_extractor = WordExtractor(trainingTexts, 100)
        words = word_extractor.GetFeatures()
        string_extractor = SubstringExtractor(trainingTexts, 0)
        strings = string_extractor.GetFeatures()
        features = pairs + words + strings
        trainer = TrainingDataSetup('restitutio', features, trainingTexts)
        classifier = BayesianClassifier(trainer)

        text1 = """ When an applicant is represented by a professional 
        representative (Article 134(1) EPC), an application for re-establishment 
        of rights under Article 122 EPC cannot be acceded to unless the representative 
        himself can show that he has taken the due care required of an applicant by 
        Article 122(1) EPC (cf. J 05/80 [OJ EPO 1981, 343], point 4 of the Reasons)."""
        text2 = """However, if the representative has entrusted to an assistant the 
        performance of routine tasks, the same strict standards of care are not expected 
        of the assistant as are expected of the applicant or his representative (cf. J 05/80 
        above, point 6 of the Reasons). Hence, a culpable error on the part of the assistant 
        made in the course of carrying out routine tasks is not to be imputed to the 
        representative if the latter has himself shown that he exercised the necessary 
        due care in dealing with his assistant. In this respect, it is incumbent upon 
        the representative to choose for the work a suitable person, properly instructed 
        in the tasks to be performed, and to exercise reasonable supervision over the 
        work (cf. J 05/80 above, point 7 of the Reasons)."""
        text3 = """By	1925	present-day	Vietnam	was	divided	into	three	parts
        under	French	colonial	rule.	The	southern	region	embracing Saigon
        and	the	Mekong	delta	was	the	colony	of	Cochin-China; the	central	area
        with	its	imperial	capital	at	Hue	was	the  protectorate	of	Annam…"""


        result1 = classifier.ClassifyText(text1)
        result2 = classifier.ClassifyText(text2)
        result3 = classifier.ClassifyText(text3)
        
        self.assertGreater(result1, 0.5)
        self.assertGreater(result2, 0.5)
        self.assertLess(result3, 0.5)               
   
          

    def test_mathematicalMethodClassifier(self):
                
        trainingTexts = TrainingTexts('mathematicalmethod')
        pair_extractor = WordPairExtractor(trainingTexts, 20)
        pairs = pair_extractor.GetFeatures()
        word_extractor = WordExtractor(trainingTexts, 10)
        words = word_extractor.GetFeatures()
        features = pairs + words
        trainer = TrainingDataSetup('mathematicalmethod', features, trainingTexts)
        classifier = BayesianClassifier(trainer)
        
        test1 = """This paragraph is about mathematical methods. It refers to Article 52(2) EPC:"""
        test2 = """ Some random paragraph that talks, if of anything at all, only about itself."""

        result1 = classifier.ClassifyText(test1)
        result2 = classifier.ClassifyText(test2)
        self.assertGreater(result1, 0.5)
        self.assertLess(result2, 0.5)



    def test_mathematicalMethodClassifierLongerText(self):
                
        trainingTexts = TrainingTexts('mathematicalmethod')
        pair_extractor = WordPairExtractor(trainingTexts, 20)
        pairs = pair_extractor.GetFeatures()
        word_extractor = WordExtractor(trainingTexts, 10)
        words = word_extractor.GetFeatures()
        features = pairs + words
        trainer = TrainingDataSetup('mathematicalmethod', features, trainingTexts)
        classifier = BayesianClassifier(trainer)

        text1 = """These are a particular example of the principle that purely abstract or intellectual 
        methods are not patentable. For example, an abstract shortcut method of division would be excluded 
        from patentability by Art. 52(2)(a) and (3). However, a calculating machine constructed to operate 
        accordingly (e.g. by executing a program designed to carry out the method) would not be excluded.
        Electrical filters designed according to a particular mathematical method would also not be excluded."""

        text2 = """Furthermore, a method for analysing the cyclical behaviour of a curve relating two parameters, 
        which are not further specified, to one another is a mathematical method as such, excluded from patentability 
        by Art. 52(2)(a) and (3), unless it uses technical means, for example, if it is computer-implemented."""

        text3 = """By	1925	present-day	Vietnam	was	divided	into	three	parts
        under	French	colonial	rule.	The	southern	region	embracing Saigon
        and	the	Mekong	delta	was	the	colony	of	Cochin-China; the	central	area
        with	its	imperial	capital	at	Hue	was	the  protectorate	of	Annam…"""


        result1 = classifier.ClassifyText(text1)
        result2 = classifier.ClassifyText(text2)
        result3 = classifier.ClassifyText(text3)
        
        self.assertGreater(result1, 0.5)
        self.assertGreater(result2, 0.5)
        self.assertLess(result3, 0.5)
        
        
             
    def test_publicPriorUseClassifier(self):
                
        trainingTexts = TrainingTexts('publicprioruse')
        pair_extractor = WordPairExtractor(trainingTexts, 20)
        pairs = pair_extractor.GetFeatures()
        word_extractor = WordExtractor(trainingTexts, 10)
        words = word_extractor.GetFeatures()
        features = pairs + words
        trainer = TrainingDataSetup('publicprioruse', features, trainingTexts)
        classifier = BayesianClassifier(trainer)
        
        test1 = """This paragraph is about public prior use. It refers to Article 54 EPC."""
        test2 = """ Some random paragraph that talks, if of anything at all, only about itself."""

        result1 = classifier.ClassifyText(test1)
        result2 = classifier.ClassifyText(test2)
        self.assertGreater(result1, 0.5)
        self.assertLess(result2, 0.5)

        

        
    def test_Serialisation(self):
        from Classifiers import Serialisers
                
        trainingTexts = TrainingTexts('restitutio')
        word_extractor = WordExtractor(trainingTexts, 10)
        words = word_extractor.GetFeatures()
        features = words
        trainer = TrainingDataSetup('restitutio', features, trainingTexts)
        classifier = BayesianClassifier(trainer)

        serialised = Serialisers.BayesianClassifierSerialise(classifier)
        deserialised = Serialisers.BayesianClassifierDeserialise(serialised)

        self.assertEqual(classifier.Classes, deserialised.Classes)
        self.assertEqual(classifier.Features, deserialised.Features)
        self.assertEqual(classifier.ClassProbabilities, deserialised.ClassProbabilities)
        self.assertEqual(classifier.FeatureProbabilitiesGivenClass, deserialised.FeatureProbabilitiesGivenClass)

                         


    def test_featureEquality(self):
        from Classifiers.Features.Features import WordClassificationFeature
        x = WordClassificationFeature('test')
        y = WordClassificationFeature('test')

        res1 = x is y
        res2 = x == y

        self.assertFalse(x is y)
        self.assertEqual(x, y)
        self.assertTrue(x == y)