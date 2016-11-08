from Classifiers.TrainingData.TrainingBase import BinaryTrainingDataBase, BinaryTrainingDate_WithExtraction_Base
from Classifiers.TrainingData import Texts


class MathematicalMethodTrainingData(BinaryTrainingDataBase):
     
    def __init__(self):
        super(MathematicalMethodTrainingData, self).__init__('mathematicalmethod')
        self._features = ['52(2)', '52(3)', 'mathamtical', 'method', 'exclude',]

        self._texts = {
            'mathematicalmethod': Texts.GetText('mathematicalmethod'),
            'other': Texts.GetText('-mathematicalmethod'),
            }

        self._testTexts = [
            """This paragraph is about mathematical methods. It refers to Article 52(2) EPC:""",

            """ Some random paragraph that talks, if of anything at all, only about itself.""",
            ]

    
class MathematicalMethodTrainingData_withExtraction(BinaryTrainingDate_WithExtraction_Base):
     
    def __init__(self):
        super(MathematicalMethodTrainingData_withExtraction, self).__init__('mathematicalmethod')
        self._extrinsicFeatures = {'52(2)', '52(3)', 'mathamtical', 'method', 'exclude',}

        self._texts = {
            'mathematicalmethod': Texts.GetText('mathematicalmethod'),
            'other' : Texts.GetText('-mathematicalmethod'),
            }

        

        self._testTexts = [
            """This paragraph is about mathematical methods. It refers to Article 52(2) EPC:""",

            """ Some random paragraph that talks, if of anything at all, only about itself.""",
            ]

       

   