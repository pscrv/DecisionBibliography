from Classifiers.TrainingData.TrainingBase import BinaryTrainingDataBase, BinaryTrainingDate_WithExtraction_Base
from Classifiers.TrainingData import Texts


class RestitutioTrainingData(BinaryTrainingDataBase):
     
    def __init__(self):
        super(RestitutioTrainingData, self).__init__('restitutio')
        self._features = ['122', 'restitutio', 'integrum', 'care', 'due', 'non-compliance']

        self._texts = {
            'restitutio': Texts.GetText('restitutio'),
            'other': Texts.GetText('-restitutio'),
            }      
       

        self._testTexts = [
            """This paragraph is about restitutio in integrum. It refers to Article 122 EPC:""",

            """ Some random paragraph that talks, if of anything at all, only about itself.""",
            ]

       
        
class RestitutioTrainingData_withExtraction(BinaryTrainingDate_WithExtraction_Base):
     
    def __init__(self):
        super(RestitutioTrainingData_withExtraction, self).__init__('restitutio')
        
        self._extrinsicFeatures = {'122', 'restitutio', 'integrum', 'care', 'due', 'non-compliance'}

        self._texts = {
            'restitutio': Texts.GetText('restitutio'),
            'other': Texts.GetText('-restitutio'),
            }
       
        
        self._testTexts = [
            """This paragraph is about restitutio in integrum. It refers to Article 122 EPC:""",

            """ Some random paragraph that talks, if of anything at all, only about itself.""",
            ]




    
   












