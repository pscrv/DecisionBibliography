from datetime import datetime
from django.db import models
from django.db.models import F


#region decision models

class DecisionGeneric(object):
    
    LANGUAGES = [('DE', 'DE'), ('EN', 'EN'), ('FR', 'FR')]
    DISTRIBUTION_CODES = [('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('', 'unknown'),]
    ALLOWED_ATTRIBUTES = {
            'CaseNumber',
            'DecisionDate', 
            'OnlineDate', 
            'Applicant', 
            'Opponents',
            'Appellants',
            'Respondents',
            'ApplicationNumber',
            'IPC',
            'Title',
            'Board',
            'Keywords',
            'Articles',
            'Rules',
            'ECLI',
            'CitedCases',
            'Distribution',
            'Headword',
            'Catchwords',
            'ProcedureLanguage',
            'DecisionLanguage',
            'Link',
            'PDFLink',
            }

    LIST_ATTRIBUTES = {
        'Opponents',
        'Respondents',
        'IPC',
        'Articles',
        'Rules',
        'CitedCases',
        }


class DecisionBibliographyManager(models.Manager):
    
    def Find_or_create(self, **kwargs):
        caseNumber = kwargs['CaseNumber']
        if not caseNumber:
            raise ValueError('Cannot create or find a DecisionBibliographyModel without a CaseNumber')

        decisionDate = kwargs['DecisionDate']
        if not decisionDate:
            raise ValueError('Cannot create or find a DecisionBibliographyModel without a DecisionDate')

        decisionLanguage = kwargs['DecisionLanguage']
        if not decisionLanguage:
            raise ValueError('Cannot create or find a DecisionBibliographyModel without a DecisionLanguage')

        
        inDB = self.filter(CaseNumber = caseNumber, DecisionDate = decisionDate, DecisionLanguage = decisionLanguage).first()
        
        if inDB:
            return inDB
        else:
            return  DecisionBibliographyModel(**kwargs)       
    

    def FilterOnlyPrLanguage(self, **kwargs):
        return self.filter(DecisionLanguage =  F('ProcedureLanguage'), **kwargs)
        

    def IsListAttribute(self, attribute):
        return attribute in DecisionGeneric.LIST_ATTRIBUTES

    

class DecisionBibliographyModel(models.Model):
    objects = DecisionBibliographyManager()
    
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
    Title = models.TextField(default = "")
    ProcedureLanguage = models.CharField(choices = DecisionGeneric.LANGUAGES, max_length = 2, default = "")
    #endregion

    #region the decision
    Board = models.CharField(max_length = 16, default = "")
    Keywords = models.TextField(default = "")
    Articles = models.CharField(max_length = 100, default = "")
    Rules = models.CharField(max_length = 100, default = "")
    ECLI = models.CharField(max_length = 20, default = "")
    CitedCases = models.CharField(max_length = 700, default = "")
    Distribution = models.CharField(choices = DecisionGeneric.DISTRIBUTION_CODES, max_length = 1, default = "")
    Headword = models.CharField(max_length = 100, default = "")
    Catchwords = models.TextField(default = "")
    DecisionLanguage = models.CharField(choices = DecisionGeneric.LANGUAGES, max_length = 2, default = "")
    #endregion

    #region links
    Link = models.URLField(max_length = 100, default = "")
    PDFLink = models.URLField(max_length = 100, default = "")
    #endregion       
    

    #region methods
    def update(self, **kwargs):        
    
        for attribute, value in kwargs.items():
            assert attribute in DecisionGeneric.ALLOWED_ATTRIBUTES, "Attribute " + attribute + " not allowed."
            if isinstance(value, str):
                value = value.strip()
            setattr(self, attribute, value)        
        self.save()
    #endregion

    def __str__(self):
        return '{} {} {}'.format(self.CaseNumber, self.DecisionLanguage, self.DecisionDate)
        

class NullBibliographyModel(DecisionBibliographyModel):
    def __init__(self, number = 'X xxxx/xx'):
        super().__init__()
        self.CaseNumber = number

    def save(self, *args, **kwargs):
        pass #do not save a null record




class DecisionTextModel(models.Model):

    Bibliography = models.OneToOneField(DecisionBibliographyModel, related_name = 'TextModel')
    
    FactsHeader = models.TextField(default = "")
    Facts = models.TextField(default = "")
    ReasonsHeader = models.TextField(default = "")
    Reasons = models.TextField(default = "")
    OrderHeader = models.TextField(default = "")
    Order = models.TextField(default = "")
    Language = models.CharField(choices = DecisionGeneric.LANGUAGES, max_length = 2, default = "")
    HasSplitText = models.BooleanField(default = False)

    
    def __str__(self):
        return 'DecisionTextModel<{}>'.format(self.Bibliography)     


class NullTextModel(DecisionTextModel):
    def __init__(self):
        super().__init__()
        self.FactsHeader = 'No text available.'
        self.ReasonsHeader = 'No text available.'
        self.OrderHeader = 'No text available.'

    def save(self, *args, **kwargs):
        pass #do not save a null record 


#endregion



#region analysis models
class AnalysisModel(models.Model):
    LastUpdate = models.DateField(auto_now = True)


class BoardAnalysisModel(AnalysisModel):    
    Board = models.CharField(max_length = 16, default = "")
    Count = models.IntegerField(default = 0)
    EarliestFive = models.CharField(max_length = 50)
    LatestFive = models.CharField(max_length = 50)
    IPC_TopFive = models.CharField(max_length = 120, default = "")
    Article_TopFive = models.CharField(max_length = 120, default = "")
    Cited_TopFive = models.CharField(max_length = 120, default = "")
    Timeline = models.TextField(default = "")    

#endregion




