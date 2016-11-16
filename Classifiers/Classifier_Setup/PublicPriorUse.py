from Classifiers.Classifier_Setup.TrainingBase import BinaryTrainingDataBase, BinaryTrainingDate_WithExtraction_Base
from Classifiers.Classifier_Setup.TrainingTexts import TrainingTexts


class PublicPriorUseTrainingData(BinaryTrainingDataBase):
     
    def __init__(self):
        super(PublicPriorUseTrainingData, self).__init__('publicprioruse', TrainingTexts('publicprioruse'))
        self._setup()

    def _setup(self):
        self._extrinsicFeatures = {'public', 'prior', 'use', '54'}
        self._testTexts = [
            """This paragraph is about public prior use. It refers to Article 54 EPC:""",
            """ Some random paragraph that talks, if of anything at all, only about itself.""",
            ]

            
class PublicPriorUseTrainingData_withExtraction(PublicPriorUseTrainingData, BinaryTrainingDate_WithExtraction_Base):
     
    def __init__(self):
        BinaryTrainingDate_WithExtraction_Base.__init__(self, 'publicprioruse', TrainingTexts('publicprioruse'))
        PublicPriorUseTrainingData._setup(self)
