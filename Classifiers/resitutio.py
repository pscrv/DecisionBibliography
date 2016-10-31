from Classifiers.Base import ClassifierBase

class RestitutioClassifier(ClassifierBase):

    def __init__(self):
        self.__phrases = ['restitutio', 'integrum',  'due', 'care', 'removal', 'cause', 'non-compliance']
        self.__articles = ['122']



 
class RestitutionTrainingDate(object):
     
    @property
    def PositiveData(self):
        return[
            """It was be concluded that the Appellant's application for re-establishment of 
            rights was duly filed within two months from the removal of the cause of non-compliance 
            with the time-limit, consisting of the appreciation by the Appellant that the renewal fee 
            for the third year had not been paid.""", 

            """In a recent Decision dated 21 October 1986 of the Legal Board of Appeal, (J 2 and 3/86, 
            "Isolated mistake- restitutio/Motorola", to be published in OJ EPO 7/1987), it is stated 
            that "Article 122 EPC is intended to ensure that in appropriate cases the loss of 
            substantive rights does not result from an isolated procedural mistake within a normally 
            satisfactory system". """,
            
            """ """,
            
            
            ]