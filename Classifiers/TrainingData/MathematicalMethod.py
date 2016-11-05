from Classifiers.TrainingData.Base import BinaryTrainingDataBase


class MathematicalMethodTrainingData(BinaryTrainingDataBase):
     
    def __init__(self):
        super(MathematicalMethodTrainingData, self).__init__('mathematicalmethod')
        self._features = ['52(2)', '52(3)', 'mathamtical', 'method', 'exclude',]

        self._texts = {
            'mathematicalmethod': [
                """Claim 1 as now worded is, in substance, directed to the encoding of data representing audio information or image information for transmission in a communication system in accordance with a codebook (ie an assignment rule) specified in the claim. Although the idea underlying the invention - the novel algorithm defining the codebook as a mathematical function - may be considered to be a mathematical method, the present claim is directed to the use of the assignment rule in the processing of audio or image signals, which are themselves physical entities. In addition, the step of "finding the group of B nearest neighbour codewords" in claim 1 includes "measuring the distance...in terms of some perceptually-related similarity of the underlying codewords". This in turn means that the entities and relationships featuring in the problem solved by the invention are not purely abstract mathematical ones. The claimed method solves a technical problem (see paragraph 4.1 below). Following the VICOM decision (T 208/84, OJ EPO 1987, 14, points 5 to 7), the board finds, therefore, that the subject-matter of this claim does not relate to a mathematical method as such and is not excluded from patentability by the provisions of Article 52(2)(a) and 52(3) EPC.""", 

                """Finally the Appellant submitted that the activity referred to in the claims would bring about a change in the physical environment in as much as a physical entity (the information stored as electric signals) is changed. This argument seems to refer to a consideration in this Board's decision in case T 208/84 (VICOM, OJ EPO 1987, 14) more in particular paragraph 5 thereof. There it was stated that "..., if a mathematical method is used in a technical process, that process is carried out on a physical entity (which may be a material object but equally an image stored as an electric signal) by some technical means... and provides as its result a certain change in that entity". It is clear from the context of the citation that the expression "physical entity" referred to a real thing i.e. an image, even if that thing was represented by an electric signal. The electric signals processed according to the present application are not of this kind but represent (part of) the information content of a document, which could be of any nature. The claimed activity does not bring about any change in the thing operated upon (i.e. the document to be abstracted) but derives therefrom a new information to be stored. Apart from that, it cannot be inferred from the citation in question that any manner of bringing about a change in a physical entity would ipso facto qualify as a technical process.""",
            
                """The question arose as to whether the subjet matter of claim 1 was directed to a purely mathematical method. If it was, then it would fall under the exclusion of Article 52(2) and 52(3) EPC. The method defined by claim 1 does not affect any physical entity, but operates solely on a sequence of numbers. It is true, that and particular implementatin will inevitably involve some physical representation of those numbers, but the invention is not concerned with such representations.""",
                ],

            'other': [
                """In the present case, a Board of Appeal has referred three questions to the Enlarged Board for the reason that two important points of law have arisen during the proceedings on the case before it. The first point of law primarily concerns the proper interpretation of Article 123(3) EPC, with particular reference to an amendment during opposition proceedings which involves a change of "category" of the claim; the second point of law primarily concerns the proper interpretation of Article 54 EPC with particular reference to a use claim where the only novel feature lies in the purpose of such use. Having regard to the purpose for which questions are referred to the Enlarged Board, as set out in Article 112 EPC, in a case such as the present, it is appropriate that the Enlarged Board should not take too narrow a view of the questions which have been referred, but should consider and answer such questions in such a way as to clarify the points of law which lie behind them.""",

                """The amendment "reflective" is supported by the original Claim 1 filed for BE, DK, FR and GB and by the expression "paper prints for viewing by reflection" on original page 6, line 34 of the application as filed.""",

                """In the board's judgment, claim 1 of this request does not have a broader scope than the scope of claims 3 and 4 as granted. In fact, the reference to the "amino acid sequence 1-527 as depicted in Fig. 5 thereof" confines this claim 1 to a precisely defined embodiment, namely the process of preparation of a human t-PA protein with the recited amino acid sequence by expression in a recombinant host organism of transforming DNA encoding it. The candidate transforming DNA encoding said protein falls within the large group of DNA sequences encoding "a 527 amino acid polypeptide having human tissue plasminogen activator function" of claims 3 and 4 as granted. Thus, the requirements of Article 123(3) EPC are met.""",            
                ]
            }

        self._testTexts = [
            """This paragraph is about mathematical methods. It refers to Article 52(2) EPC:""",

            """ Some random paragraph that talks, if of anything at all, only about itself.""",
            ]

       

   