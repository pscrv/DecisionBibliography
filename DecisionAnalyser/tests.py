import django
from django.test import TestCase

from Classifiers.Bayesian import BayesianClassifier

# TODO: Configure your database in settings.py and sync before running tests.


class DATest(TestCase):
    """Tests for the application views."""

    if django.VERSION[:2] >= (1, 7):
        # Django 1.7 requires an explicit setup() when running tests in PTVS
        @classmethod
        def setUpClass(cls):    
            super(DATest, cls).setUpClass()
            django.setup()

    def test_CanMakeBayesianClassifier(self):
        classifier = self.__makeRestitutioClassifier()
        self.assertTrue(classifier)

        
    def test_Can_De_SerialiseBayesianClassifier(self):
        from Classifiers.Serialisers import BayesianClassifierSerialise, BayesianClassifierDeserialise

        classifier = self.__makeRestitutioClassifier()
        ser = BayesianClassifierSerialise(classifier)
        des = BayesianClassifierDeserialise(ser)
        self.assertEqual(classifier.Classes, des.Classes)
        self.assertEqual(classifier.Features, des.Features)
        

    def test_CanSaveAndRestoreBayesianClassifier(self):
        from Classifiers.Serialisers import BayesianClassifierSerialise, BayesianClassifierDeserialise
        from DecisionAnalyser.models import ClassifierSerialisationModel

        classifier = self.__makeRestitutioClassifier()
        ser = BayesianClassifierSerialise(classifier)
        model = ClassifierSerialisationModel(Name = 'restitutio', Serialised=ser)
        model.save()
        retrieved = ClassifierSerialisationModel.objects.get(Name = 'restitutio')
        des = BayesianClassifierDeserialise(retrieved.Serialised)
        self.assertEqual(classifier.Classes, des.Classes)
        self.assertEqual(classifier.Features, des.Features)


    def test_CanSaveAndRetrieveUsingManager(self):
        from DecisionAnalyser.models import ClassifierSerialisationModel

        classifier = self.__makeRestitutioClassifier()
        ClassifierSerialisationModel.objects.SaveBayesianClassifier('rstto', classifier)
        des = ClassifierSerialisationModel.objects.RetrieveBayesianclassifier('rstto')
        self.assertEqual(classifier.Classes, des.Classes)
        self.assertEqual(classifier.Features, des.Features)
        
    def test_IfNoTrainingText(self):
        classifier = BayesianClassifier.MakeClassifier('stupidnamethatdoesnotexist', ['dummyword'], [('dummyword1', 'dummyword2')])
        self.assertTrue(classifier)

    def test_CanSaveAndRetreiveFromMakeClassifier(self):
        from DecisionAnalyser.models import ClassifierSerialisationModel
        classifier = BayesianClassifier.MakeClassifier('restitutio', ['restitutio', 'integrum'], [('122', 'EPC'), ('due', 'care')])
        ClassifierSerialisationModel.objects.SaveBayesianClassifier('weirdname', classifier)
        des = ClassifierSerialisationModel.objects.RetrieveBayesianclassifier('weirdname')
        self.assertEqual(classifier.Classes, des.Classes)
        self.assertEqual(classifier.Features, des.Features)
        self.assertEqual(classifier.ClassProbabilities, des.ClassProbabilities)
        self.assertEqual(classifier.FeatureProbabilitiesGivenClass, des.FeatureProbabilitiesGivenClass)
        


    def __makeRestitutioClassifier(self):
        featureWords = ['restitutio', 'integrum', 'mistake', ]
        featureWordPairs = [('122', 'EPC'), ('due', 'care'),]
        return BayesianClassifier.MakeClassifier('restitutio', featureWords, featureWordPairs)


    
class DecisionAnalyserTest(TestCase):
    """Tests for the application views."""

    if django.VERSION[:2] >= (1, 7):
        # Django 1.7 requires an explicit setup() when running tests in PTVS
        @classmethod
        def setUpClass(cls):    
            super(DecisionAnalyserTest, cls).setUpClass()
            django.setup()

    def test_CanGetDecisionTexts(self):
        
        from app.DBProxy import DecisionModelProxy
        decision = DecisionModelProxy.GetDecisionListFromCaseNumber('T 0027/86').first()

        from DecisionAnalyser.EPOAnalyser import TextAnalyser
        from Classifiers.Bayesian import BayesianClassifier
        classifier = BayesianClassifier.MakeClassifier(
            'restitutio', 
            ['restitutio', 'integrum', 're-establish'], 
            [('122', 'EPC'), ('due', 'care'), ('re-', 'establish'), ('re', 'establish')]
            )
        analyser = TextAnalyser.Analyser(en_classifier = classifier)
        texts = analyser.Analyse_Decision(decision)
        self.assertTrue(texts['Facts'])
        self.assertTrue(texts['Reasons'])
        self.assertTrue(texts['Order'])

        
    def test_ExtractCasenumbersFromText(self):
        casenumber = "G 0002/88"
        
        from app.DBProxy import DecisionModelProxy
        decision = DecisionModelProxy.GetRepresentativeForCaseNumber(casenumber)
        citedInText = DecisionModelProxy.ExtractCasenumbersFromText(decision)
        x = 1
        






