from DecisionsPlus import models

def GetModelCounts():
    return {
        'base': models.BibliographyBaseModel.objects.count(),
        'lang': models.BibliographyLanguageVersionModel.objects.count(),
        'text': models.TextModel.objects.count(),
        'supp': models.CitationSupplementModel.objects.count(),
        }