from Classifiers.Classifier_Setup.TrainingBase import BinaryTrainingDataBase, BinaryTrainingDate_WithExtraction_Base
from Classifiers.Classifier_Setup.TrainingTexts import TrainingTexts


class MathematicalMethodTrainingData(BinaryTrainingDataBase):
     
    def __init__(self):
        super(MathematicalMethodTrainingData, self).__init__('mathematicalmethod', TrainingTexts('mathematicalmethod'))
        self._setup()

    def _setup(self):
        self._extrinsicFeatures = {'52(2)', '52(3)', 'mathematical', 'method', 'exclude',}
        self._testTexts = [
            """This paragraph is about mathematical methods. It refers to Article 52(2) EPC:""",
            """ Some random paragraph that talks, if of anything at all, only about itself.""",
            ]
        

class MathematicalMethodTrainingData_withExtraction(MathematicalMethodTrainingData, BinaryTrainingDate_WithExtraction_Base):
     
    def __init__(self):
        BinaryTrainingDate_WithExtraction_Base.__init__(self, 'mathematicalmethod', TrainingTexts('mathematicalmethod'))
        MathematicalMethodTrainingData._setup(self)
   
    

       

   