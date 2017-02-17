from Decisions.models import DecisionTextModel

def GetCitationStatus():
    from Decisions.models import DecisionBibliographyModel
    from Decisions import Formatters
        
    textcases = DecisionTextModel.objects.all()
    db_casenumbers = set(DecisionBibliographyModel.objects.values_list('CaseNumber', flat = True))

    citations = {
        'textcount': len(textcases),
        'good': {},
        'bad': {},
        'extra': {},
        'missing': {},
    }

    for text in textcases:
        case = text.Bibliography
        
        citedCases = set(Formatters.formatCaseNumber(x) for x in case.CitedCases.split(',') if x != '')
        textcitations = __extractCaseCitationsFromText('::'.join([text.Facts, text.Reasons, text.Order]))
        for citation in textcitations:
            if citation in db_casenumbers:
                citations['good'][case.CaseNumber] = set.union(citations['good'].get(case.CaseNumber, set()), {citation})
            else:
                citations['bad'][case.CaseNumber] = set.union(citations['bad'].get(case.CaseNumber, set()), {citation})

            if citation not in citedCases:
                citations['extra'][case.CaseNumber] = set.union(citations['extra'].get(case.CaseNumber, set()),{citation})

        for citedcase in citedCases:
            if citedcase not in textcitations:
                citations['missing'][case.CaseNumber] = set.union(citations['missing'].get(case.CaseNumber, set()), {citation})
            
    return citations

 
def __extractCaseCitationsFromText(text):
    import re
    from Decisions import Formatters
    finder = re.compile(r'\b([DGJRTW]\s*\d{1,4}/\d{2}\b)', re.IGNORECASE)
    matches = re.findall(finder, text)
    return set(Formatters.formatCaseNumber(x) for x in matches)