import re
from Decisions import Formatters
from Decisions.models import DecisionBibliographyModel, DecisionSupplementaryModel


class SupplementManager(object):

    def __init__(self):
        self.__allCaseNumbers = DecisionBibliographyModel.objects.values_list('CaseNumber', flat = True)
        self.__bibliographiesWithSupplements = DecisionBibliographyModel.objects.exclude(SupplementModel = None)
        

    def AddCited(self, bibliography):
        if not hasattr(bibliography, 'SupplementModel'):
            bibliography.SupplementModel = DecisionSupplementaryModel()
        
        bib_cited_inDB, bib_cited_notInDB = self.__splitCaseNumbers(bibliography.CitedCases.split(','))
        bibliography.SupplementModel.CitedCases_NotInDB = bib_cited_notInDB
        
        texts = bibliography.TextModel
        text_cited_inDB, text_cited_notInDB = self.__extractCaseCitationsFromText(texts)
        bibliography.SupplementModel.CasesExtractedFromTexts_InDB = text_cited_inDB
        bibliography.SupplementModel.CasesExtractedFromTexts_NotInDB = text_cited_notInDB
        bibliography.SupplementModel.save()


    def AddCiting(self, bibliography):
        if not hasattr(bibliography, 'SupplementModel'):
            return
        bib_citing = ','.join(
            x.CaseNumber 
            for x in DecisionBibliographyModel.objects.filter(CitedCases__contains = bibliography.CaseNumber)
            )
        text_citing = ','.join(
            x.CaseNumber 
            for x in self.__bibliographiesWithSupplements.filter(SupplementModel__CasesExtractedFromTexts_InDB__contains = bibliography.CaseNumber)
            )                                
        bibliography.SupplementModel.CitingCases_Bibliography = bib_citing
        bibliography.SupplementModel.CitingCases_Text = text_citing
        bibliography.SupplementModel.save()



    def __extractCaseCitationsFromText(self, textmodel):
        finder = re.compile(r'\b([DGJRTW]\s*\d{1,4}/\d{2}\b)', re.IGNORECASE)                
        compositetext = ' '.join([textmodel.Facts, textmodel.Reasons, textmodel.Order])
        matches = re.findall(finder, compositetext)

        caseNumbers = set(Formatters.formatCaseNumber(x) for x in matches)
        return self.__splitCaseNumbers(caseNumbers)


    def __splitCaseNumbers(self, cn_list):
        inDB = []
        notInDB = []
        for cn in cn_list:
            if cn == '':
                continue
            if cn in self.__allCaseNumbers:
                inDB.append(cn)
            else:
                notInDB.append(cn)
        return inDB, notInDB