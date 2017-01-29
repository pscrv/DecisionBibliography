from Decisions.models import DecisionBibliographyModel

DECISIONTYPELETTERS = 'DGJRTW'

def FindCaseNumbers():
    caseNumbers = DecisionBibliographyModel.objects.values('CaseNumber')
    caseNumberSet = set(x['CaseNumber'] for x in caseNumbers)
    return caseNumberSet


def FindCaseNumbersOfType(typeletter):
    if typeletter not in DECISIONTYPELETTERS:
        return 0
    caseNumbers = FindCaseNumbers()
    caseNumbersOfType = [x for x in caseNumbers if x[0] == typeletter]
    return caseNumbersOfType


def FindCitedCaseNumbers():
    caseNumberSet = FindCaseNumbers()
    citedCaseNumbers = DecisionBibliographyModel.objects.values('CitedCases')
    citedCaseNumberSet = set(y.strip() for x in citedCaseNumbers for y in x['CitedCases'].split(',') if y.strip() != '')
    return citedCaseNumberSet


def FindCitedCasesNotInDB():
    caseNumberSet = FindCaseNumbers()
    citedCaseNumberSet = FindCitedCaseNumbers()
    citedCaseNumbersNotInDB = citedCaseNumberSet.difference(caseNumberSet)
    return citedCaseNumbersNotInDB


def CountRecords():
    return DecisionBibliographyModel.objects.count()


def CountCaseNumbers():
    return len(FindCaseNumbers())


def CountDecisionType(typeletter):
    if typeletter not in DECISIONTYPELETTERS:
        return 0
    return DecisionBibliographyModel.objects.filter(CaseNumber__startswith=typeletter).count()


def CountCaseNumbersForType(typeletter):
    return len(FindCaseNumbersOfType(typeletter))



