from Decisions.EpoSearchFacade import EpoSearchFacade
from Decisions.EpoConverter import EpoConverter
from Decisions.models import DecisionBibliographyModel, DecisionTextModel



class TextGetter(object):

    def Get_Text(self, bibliography):
        searcher = EpoSearchFacade()
        converter = EpoConverter()

        inDB = DecisionTextModel.objects.filter(Bibliography = bibliography)
        if inDB:
            return
        
        try:
            response = searcher.SearchDecisionText(bibliography.Link)
            decisionText = converter.ResponseToDecisionText(response)
            decisionText.Bibliography = bibliography
            decisionText.Language = bibliography.ProcedureLanguage
        except Exception as ex:
            t = type(ex)      
            return None

        decisionText.save()
        return decisionText

           


