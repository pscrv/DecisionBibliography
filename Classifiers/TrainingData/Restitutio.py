from Classifiers.TrainingData.TrainingBase import BinaryTrainingDataBase, BinaryTrainingDate_WithExtraction_Base
from Classifiers.TrainingData import Texts


class RestitutioTrainingData(BinaryTrainingDataBase):
     
    def __init__(self):
        super(RestitutioTrainingData, self).__init__('restitutio')
        self._setup()

    def _setup(self):
        self._extrinsicFeatures = {'122', 'restitutio', 'integrum', 'care', 'due', 'non-compliance'}
        self._testTexts = [
            """This paragraph is about restitutio in integrum. It refers to Article 122 EPC:""",

            """ Some random paragraph that talks, if of anything at all, only about itself.""",
            ]

       
        
class RestitutioTrainingData_withExtraction(RestitutioTrainingData, BinaryTrainingDate_WithExtraction_Base):
     
    def __init__(self):
        BinaryTrainingDate_WithExtraction_Base.__init__(self, 'restitutio')
        RestitutioTrainingData._setup(self)


    
   












