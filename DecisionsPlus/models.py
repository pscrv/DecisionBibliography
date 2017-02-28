from django.db import models


class DecisionGeneric():
    
    LANGUAGES = [('DE', 'DE'), ('EN', 'EN'), ('FR', 'FR')]
    DISTRIBUTION_CODES = [('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('', 'unknown'),]
   

class BibliographyBaseModel(models.Model):
    
    CaseNumber = models.CharField(max_length = 16, default = "")
    
    #region dates
    DecisionDate = models.DateField(blank=True, null=True)
    OnlineDate = models.DateField(blank=True, null=True)
    #endregion

    #region parties
    Applicant = models.CharField(max_length = 50, default = "")
    Opponents = models.CharField(max_length = 200, default = "")
    Appellants = models.CharField(max_length = 200, default = "")
    Respondents = models.CharField(max_length = 200, default = "")
    #endregion

    #region application
    ApplicationNumber = models.CharField(max_length = 15, default = "")
    IPC = models.CharField(max_length = 50, default = "")
    ProcedureLanguage = models.CharField(choices = DecisionGeneric.LANGUAGES, max_length = 2, default = "")
    #endregion

    #region the decision
    Board = models.CharField(max_length = 16, default = "")
    Articles = models.CharField(max_length = 100, default = "")
    Rules = models.CharField(max_length = 100, default = "")
    ECLI = models.CharField(max_length = 20, default = "")
    CitedCases = models.CharField(max_length = 700, default = "")
    Distribution = models.CharField(choices = DecisionGeneric.DISTRIBUTION_CODES, max_length = 1, default = "")
    #endregion


    FieldNames = [
            'CaseNumber',
            'DecisionDate', 
            'OnlineDate', 
            'Applicant', 
            'Opponents',
            'Appellants',
            'Respondents',
            'ApplicationNumber',
            'IPC',
            'Board',
            'Articles',
            'Rules',
            'ECLI',
            'CitedCases',
            'Distribution',
            'ProcedureLanguage',
            ]            
    
    def __str__(self):
        return '{} {}'.format(self.CaseNumber, self.DecisionDate)



class BibliographyLanguageVersionModel(models.Model):    
    
    BibliographyBase = models.ForeignKey(
        BibliographyBaseModel, 
        related_name = 'LanguageModel',
        on_delete = models.CASCADE,
        )
    DecisionLanguage = models.CharField(choices = DecisionGeneric.LANGUAGES, max_length = 2, default = "")
    Title = models.TextField(default = "")
    Keywords = models.TextField(default = "")
    Headword = models.CharField(max_length = 100, default = "")
    Catchwords = models.TextField(default = "")
    Link = models.URLField(max_length = 100, default = "")
    PDFLink = models.URLField(max_length = 100, default = "")

    FieldNames =  [
            'Title',
            'Keywords',
            'Headword',
            'Catchwords',
            'DecisionLanguage',
            'Link',
            'PDFLink',
            ]

    def __str__(self):
        return '{} {} {}'.format(self.BibliographyBase.CaseNumber, self.BibliographyBase.DecisionDate, self.DecisionLanguage)


    
class TextModel(models.Model):

    Bibliography = models.OneToOneField(
        BibliographyLanguageVersionModel, 
        related_name = 'TextModel',
        primary_key = True,
        on_delete = models.CASCADE,
        )
    
    FactsHeader = models.TextField(default = "")
    Facts = models.TextField(default = "")
    ReasonsHeader = models.TextField(default = "")
    Reasons = models.TextField(default = "")
    OrderHeader = models.TextField(default = "")
    Order = models.TextField(default = "")
    HasSplitText = models.BooleanField(default = False)

    FieldNames = [
           'FactsHeader',
           'Facts',
           'ReasonsHeader',
           'Reasons',
           'OrderHeader',
           'Order',
           'HasSplitText',
           ]
           
    
    def __str__(self):
        return 'TextModel<{}>'.format(self.Bibliography)     



class CitationSupplementModel(models.Model):

    Bibliography = models.OneToOneField(
        BibliographyLanguageVersionModel, 
        related_name = 'CitationSupplementModel',
        primary_key = True,
        on_delete = models.CASCADE,
        )

    CitedCases_notInDB =  models.TextField(default = "")
    
    TextCited_inDB =  models.TextField(default = "")
    TextCited_notInDB =  models.TextField(default = "")
   
    BibliographyCiting =  models.TextField(default = "")
    TextCiting =  models.TextField(default = "")

   
    FieldNames = [
        'CitedCases_notInDB',
        'TextCited_inDB',
        'TextCited_notInDB',
        'BibliographyCiting',
        'TextCiting',
        ]

    
    def __str__(self):
        return 'CitationSupplementModel<{}>'.format(self.Bibliography)


