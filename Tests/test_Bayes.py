import unittest

class test_Bayes(unittest.TestCase):
        
    def test_RestitutioClassifier(self):
        from Classifiers.Bayesian import BayesianClassifier
        from Classifiers.TrainingData.Restitutio import RestitutioTrainingData 

        classifier = BayesianClassifier(RestitutioTrainingData())
        result = classifier.GetTestClassification()
        restitutio = [x for x, (y, z) in result.items() if y == 'restitutio']
        self.assertEqual(len(restitutio), 1)
        self.assertTrue('122' in restitutio[0])

    def test_RestitutioClassifierLongerText(self):
        from Classifiers.Bayesian import BayesianClassifier
        from Classifiers.TrainingData.Restitutio import RestitutioTrainingData
        classifier = BayesianClassifier(RestitutioTrainingData())

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
        
        self.assertEqual(result1[0], 'restitutio')
        self.assertEqual(result2[0], 'restitutio')
        self.assertEqual(result3[0], 'other')

    def test_MathematicalMethodClassifier(self):
        from Classifiers.Bayesian import BayesianClassifier
        from Classifiers.TrainingData.MathematicalMethod import MathematicalMethodTrainingData

        classifier = BayesianClassifier(MathematicalMethodTrainingData())
        result = classifier.GetTestClassification()
        restitutio = [x for x, (y, z) in result.items() if y == 'mathematicalmethod']
        self.assertEqual(len(restitutio), 1)
        self.assertTrue('52(2)' in restitutio[0])



    def test_MathematicalMethodClassifierLongerText(self):
        from Classifiers.Bayesian import BayesianClassifier
        from Classifiers.TrainingData.MathematicalMethod import MathematicalMethodTrainingData
        classifier = BayesianClassifier(MathematicalMethodTrainingData())

        text1 = """These are a particular example of the principle that purely abstract or intellectual methods are not patentable. For example, an abstract shortcut method of division would be excluded from patentability by Art. 52(2)(a) and (3). However, a calculating machine constructed to operate accordingly (e.g. by executing a program designed to carry out the method) would not be excluded. Electrical filters designed according to a particular mathematical method would also not be excluded."""

        text2 = """Furthermore, a method for analysing the cyclical behaviour of a curve relating two parameters, which are not further specified, to one another is a mathematical method as such, excluded from patentability by Art. 52(2)(a) and (3), unless it uses technical means, for example, if it is computer-implemented."""

        text3 = """By	1925	present-day	Vietnam	was	divided	into	three	parts
        under	French	colonial	rule.	The	southern	region	embracing Saigon
        and	the	Mekong	delta	was	the	colony	of	Cochin-China; the	central	area
        with	its	imperial	capital	at	Hue	was	the  protectorate	of	Annam…"""


        result1 = classifier.ClassifyText(text1)
        result2 = classifier.ClassifyText(text2)
        result3 = classifier.ClassifyText(text3)
        
        self.assertEqual(result1[0], 'mathematicalmethod')
        self.assertEqual(result2[0], 'mathematicalmethod')
        self.assertEqual(result3[0], 'other')




