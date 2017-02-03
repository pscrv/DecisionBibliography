from . EpoSearchFacade import EpoSearchFacade
from . EpoConverter import EpoConverter
from . models import DecisionBibliographyModel, DecisionTextModel



class TextGetter(object):

    #TODO: Big re-write
    def Get_Text(self, decision):
        searcher = EpoSearchFacade()
        converter = EpoConverter()
        
        try:
            response = searcher.SearchDecisionText(decision.Link)
            decisionText = converter.ResponseToDecisionText(response)
            decisionText.Bibliography = DecisionBibliographyModel.objects.filter(pk = decision.pk).first()
            decisionText.Language = decision.ProcedureLanguage
        except Exception as ex:
            t = type(ex)      
            return None

        inDB = DecisionTextModel.objects.filter(
                Bibliography = decisionText.Bibliography,
                Language = decision.ProcedureLanguage).first()

        if inDB:
            pass  # already here
        else:
            decisionText.save()

        return decisionText

           


