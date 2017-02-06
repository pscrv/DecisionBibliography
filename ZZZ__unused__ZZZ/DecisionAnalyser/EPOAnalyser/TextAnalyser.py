
class Analyser(object):

    def __init__(self, name = None, de_classifier = None, en_classifier = None, fr_classifier = None):
        self.__analyser = {}
        self.__analyser['DE'] = de_classifier
        self.__analyser['EN'] = en_classifier
        self.__analyser['FR'] = fr_classifier
        self.__language = None
        if name: 
            self.__name = name
        elif en_classifier:
            self.__name = en_classifier.Name
        else:
            self.__name = ""

    @property
    def Name(self):
        return self.__name


    def Analyse_Decision(self, decision):
         self.__language = decision.DecisionLanguage

         from app.DBProxy import DecisionModelProxy
         texts = DecisionModelProxy.GetTextFromDecision(decision)

       
         return {
             'Facts' : [self.__classifyparagraph(x) for x in texts.Facts.split('\n\n')],
             'Reasons' : [self.__classifyparagraph(x) for x in texts.Reasons.split('\n\n')],
             'Order' : [self.__classifyparagraph(x) for x in texts.Order.split('\n\n')],
             }
         
    def __classifyparagraph(self, para):
        return (para, self.__analyser[self.__language].ClassifyText(para))


class NullAnalyser(Analyser):

    def Analyse_Decision(self, decision):
        from app.DBProxy import DecisionModelProxy
        texts = DecisionModelProxy.GetTextFromDecision(decision)
        return {
             'Facts' : [(x, 0.0) for x in texts.Facts.split('\n\n')],
             'Reasons' : [(x, 0.0) for x in texts.Reasons.split('\n\n')],
             'Order' : [(x, 0.0) for x in texts.Order.split('\n\n')],
             }


