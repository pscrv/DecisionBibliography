
class Analyser(object):

    def __init__(self, de_classifier = None, en_classifier = None, fr_classifier = None):
        self.__analyser = {}
        self.__analyser['DE'] = de_classifier
        self.__analyser['EN'] = en_classifier
        self.__analyser['FR'] = fr_classifier
        self.__language = None

    def Analyse_Decision(self, decision):
         self.__language = decision.DecisionLanguage
         textparts = ['Facts', 'Reasons', 'Order']

         from app.DBProxy import DecisionModelProxy
         texts = DecisionModelProxy.GetTextFromDecision(decision)
         return {
             'Facts' : [self.__classifyparagraph(x) for x in texts.Facts.split('\n\n')],
             'Reasons' : [self.__classifyparagraph(x) for x in texts.Reasons.split('\n\n')],
             'Order' : [self.__classifyparagraph(x) for x in texts.Order.split('\n\n')],
             }
         
    def __classifyparagraph(self, para):
        return (para, self.__analyser[self.__language].ClassifyText(para))

