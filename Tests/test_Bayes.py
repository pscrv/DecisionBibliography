import unittest

class test_Bayes(unittest.TestCase):
        
    def test_RestitutioClassifier(self):
        from Classifiers.restitutio import BayesianClassifier
        from Classifiers.TrainingData.Restitutio import RestitutioTrainingData 

        classifier = BayesianClassifier(RestitutioTrainingData())
        result = classifier.GetTestClassification()
        restitutio = [x for x, y in result.items() if y == 'restitutio']
        self.assertEqual(len(restitutio), 1)
        self.assertTrue('122' in restitutio[0])

    def test_RestitutioClassifierLongerText(self):
        from Classifiers.restitutio import BayesianClassifier
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
        
        self.assertEqual(result1, 'restitutio')
        self.assertEqual(result2, 'restitutio')
        self.assertEqual(result3, 'other')







