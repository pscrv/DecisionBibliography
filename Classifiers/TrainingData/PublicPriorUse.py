from Classifiers.TrainingData.TrainingBase import BinaryTrainingDataBase, BinaryTrainingDate_WithExtraction_Base
from Classifiers.TrainingData import Texts


class PublicPriorUseTrainingData(BinaryTrainingDataBase):
     
    def __init__(self):
        super(PublicPriorUseTrainingData, self).__init__('publicprioruse')
        self._features = ['public', 'prior', 'use', '54']

        self._texts = {
            'publicprioruse': Texts.GetText('publicprioruse'),
            'other': Texts.GetText('-publicprioruse'),
            }

        self._testTexts = [
            """This paragraph is about public prior use. It refers to Article 54 EPC:""",

            """ Some random paragraph that talks, if of anything at all, only about itself.""",
            ]

            
class PublicPriorUseTrainingData_withExtraction(BinaryTrainingDate_WithExtraction_Base):
     
    def __init__(self):
        super(PublicPriorUseTrainingData_withExtraction, self).__init__('publicprioruse')
        self._extrinsicFeatures = {'public', 'prior', 'use', '54',}

        self._texts = {
            'publicprioruse': Texts.GetText('publicprioruse'),
            'other' : Texts.GetText('-publicprioruse'),
            }

        

        self._testTexts = [
            """This paragraph is about public prior use. It refers to Article 54 EPC:""",

            """ Some random paragraph that talks, if of anything at all, only about itself.""",
            ]
