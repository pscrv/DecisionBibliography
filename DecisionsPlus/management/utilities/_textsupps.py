import re
from Decisions import Formatters

from DecisionsPlus.models import BibliographyBaseModel, BibliographyLanguageVersionModel, TextModel, CitationSupplementModel


__allCaseNumbers = BibliographyBaseModel.objects.values_list('CaseNumber', flat = True).distinct()


def AddDecisionPlusTextAndSuppFromDecisionsDB(oldbib):

        languageModels = BibliographyLanguageVersionModel.objects.filter(
            BibliographyBase__CaseNumber = oldbib.CaseNumber,
            BibliographyBase__DecisionDate = oldbib.DecisionDate,
            DecisionLanguage = oldbib.DecisionLanguage)

        languageModel = languageModels.first()
        if len(languageModels) > 1:
            languageModels[1:].delete()

        if hasattr(languageModel, 'TextModel'):
            languageModel.TextModel.delete()
                
        if hasattr(languageModel, 'CitationSupplementModel'):
            languageModel.CitationSupplementModel.delete()
            
        if hasattr(oldbib, 'TextModel'):
            textdict = {f: getattr(oldbib.TextModel, f) for f in TextModel.FieldNames}
            text = TextModel(**textdict)
            text.Bibliography = languageModel
            text.save()                
            AddSupp(languageModel)                
   



def AddSupp(languagemodel):
    if not hasattr(languagemodel, 'TextModel'):
        raise AttributeError('Cannot add a supplement if there is no text.')
        
    decision_base = languagemodel.BibliographyBase
    decision_text = languagemodel.TextModel
    decision_supp = getattr(languagemodel, 'SupplementModel', CitationSupplementModel())

    bibCited_inDb, bibCited_notInDb = __splitCaseNumbers(decision_base.CitedCases.split(','))
    textCited_inDB, textCited_notInDB = __getTextCitations(decision_text)

    bibCiting = ','.join(
            x.CaseNumber
            for x in BibliographyBaseModel.objects.filter(CitedCases__contains = decision_base.CaseNumber)
            )
    text_citing = ','.join(
            x.Bibliography.BibliographyBase.CaseNumber
            for x in CitationSupplementModel.objects.filter(TextCited_inDB__contains = decision_base.CaseNumber)
            )   

    decision_supp.Bibliography = languagemodel
    decision_supp.CitedCases_notInDB = bibCited_notInDb
    decision_supp.TextCited_inDB = textCited_inDB
    decision_supp.TextCited_notInDB = textCited_notInDB
    decision_supp.BibliographyCiting = bibCiting
    decision_supp.TextCiting = text_citing
    decision_supp.save()

    
    for cited in decision_supp.TextCited_inDB:
        cases = BibliographyLanguageVersionModel.objects.filter(BibliographyBase__CaseNumber = cited).exclude(CitationSupplementModel = None)        
        for case in cases:
            citing_set = set(filter(bool, case.CitationSupplementModel.TextCiting.split(',')))
            citing_set.add(decision_base.CaseNumber)
            case.CitationSupplementModel.TextCiting = ','.join(citing_set)
            case.save()
    

def __splitCaseNumbers(cn_list):
    inDB = []
    notInDB = []
    for cn in cn_list:
        if cn == '':
            continue
        if cn in __allCaseNumbers:
            inDB.append(cn)
        else:
            notInDB.append(cn)
    return ','.join(inDB), ','.join(notInDB)


def __getTextCitations(textmodel):    
    finder = re.compile(r'\b([DGJRTW]\s*\d{1,4}/\d{2}\b)', re.IGNORECASE)                
    compositetext = ' '.join([textmodel.Facts, textmodel.Reasons, textmodel.Order])
    matches = re.findall(finder, compositetext)

    caseNumbers = set(Formatters.formatCaseNumber(x) for x in matches)
    return __splitCaseNumbers(caseNumbers)



