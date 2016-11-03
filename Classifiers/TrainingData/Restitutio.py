import abc

class BinaryTrainingDataBase(abc.ABC):

    def __init__(self, name):
        self._name = name
        self._classes = [name, 'other']
        self._features = []
        self._testTexts = []
        self._texts = {
            name : [],
            'other' : []
            }


    def GetTrainingTexts(self, cl):
        return self._texts.get(cl, [])

    def GetClassProportion(self, cl):
        texts = self.GetTrainingTexts(cl)
        return len(texts) / self.TotalTextCount

    @property
    def Classes(self):
        return self._classes

    @property
    def Features(self):
        return self._features

    @property
    def FeatureCount(self):
        return len(self._features)

    @property
    def PositiveData(self):
        return self._positiveTexts

    @property
    def NegativeData(self):
        return self._negativeTexts

    @property
    def TestData(self):
        return self._testTexts
    
    @property
    def TotalTextCount(self):
        return len(self._texts[self._name]) + len(self._texts['other'])

    @property
    def PositiveProportion(self):
        return len(self._texts[self._name]) / self.TotalTextCount

    @property
    def NegativeProportion(self):
        return len(self._texts['other']) / self.TotalTextCount

    def SplitTextsBy(self, cl, term):
        if cl == self._name:
            source = self.PositiveData
        else:
            source = self.NegativeData
        return (
            ' '.join([x for x in source if term in x]),
            ' '.join([x for x in source if term not in x]),
            )



class RestitutioTrainingData(BinaryTrainingDataBase):
     
    def __init__(self):
        super(RestitutioTrainingData, self).__init__('restitutio')
        self._features = ['122', 'restitutio', 'integrum', 'care', 'due', 'non-compliance']

        self._texts = {
            'restitutio': [
                """It was be concluded that the Appellant's application for re-establishment of 
                rights was duly filed within two months from the removal of the cause of non-compliance 
                with the time-limit, consisting of the appreciation by the Appellant that the renewal fee 
                for the third year had not been paid.""", 

                """In a recent Decision dated 21 October 1986 of the Legal Board of Appeal, (J 2 and 3/86, 
                "Isolated mistake- restitutio/Motorola", to be published in OJ EPO 7/1987), it is stated 
                that "Article 122 EPC is intended to ensure that in appropriate cases the loss of 
                substantive rights does not result from an isolated procedural mistake within a normally 
                satisfactory system". """,
            
                """However, the two month period laid down in Article 122 EPC was clearly designed to 
                enable parties to carry out the necessary investigations and consultations, as well as 
                to prepare the documentation for submission of a request under Article 122 EPC. The date 
                of removal of the cause of non-compliance, therefore, cannot be set at the date when these 
                preparations have been completed to the point where the representative is about to submit 
                a request for re- establishment, but must be a date before that.""",
                ],

            'other': [
                """ However, the passage introduced by "such that.." is ambiguous as it seems to imply 
                that particular conditions have to be respected or particular measures have to be taken 
                for obtaining images having detail without, however, specifying these conditions or measures. 
                The Appellant submitted during oral proceedings that all the embodiments of the subject-matter 
                of Claim 1 having the physical technical features as defined would produce images having 
                detail when formed in the high density shadow region of at least one dye-image forming layer. 
                This would mean that, hence, this effect is necessarily obtained by the said physical technical 
                features; consequently, the functionally defined feature relating to a layer "having detail" 
                would not be distinguishing and, therefore, it would be redundant.""",

                """The general rule is that a legal provision, here Rule 25 EPC, is to be applied by a tribunal, 
                here this board, on the interpretation it considers correct, to all situations arising during 
                the time the legal provision is in force. The main request of the Appellant must thus fail, 
                unless some special exception derived from the principle of the protection of legitimate 
                expectations exists from which the Appellant could benefit.""",

                """The fact that the third statement (c) is not wholly conterminous with the originally filed 
                Claim 1, does not imply that the air space dielectric, which is mentioned in statement (c) and 
                in Claim 1 as originally filed, could be omitted. Nor does it imply that statement (a) should 
                be interpreted as a statement of invention instead of statement (c). In fact, of the three 
                statements (a), (b) and (c), statement (c) is the one which comes closest to Claim 1 as originally 
                filed.""",            
                ]
            }

        self._testTexts = [
            """This paragraph is about restitutio in integrum. It refers to Article 122 EPC:""",

            """ Some random paragraph that talks, if of anything at all, only about itself.""",
            ]

       

   