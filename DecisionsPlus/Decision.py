from DecisionsPlus.models import BibliographyBaseModel, BibliographyLanguageVersionModel, TextModel, CitationSupplementModel

class DecisionProxy:
    
    __map = {
        BibliographyBaseModel: 'BibliographyBase',
        TextModel: 'TextModel',
        CitationSupplementModel: 'CitationSupplementModel'
        }

    __splitFields = ['Facts', 'Reasons', 'Order']


    def __init__(self, languageversion):
        self._languageversion = languageversion

        if languageversion is None:
            return        
        if not isinstance(languageversion, BibliographyLanguageVersionModel):
            raise ValueError('languageversion must be an instance of BibliographyLanguageVersionModel but is {}'.format(type(languageversion)))
        
        self.pk = languageversion.pk  
        self.CaseNumbver = languageversion.BibliographyBase.CaseNumber
        self.DecisionDate = languageversion.BibliographyBase.DecisionDate
        self.DecisionLanguage = languageversion.DecisionLanguage
                    
  

    def __getattr__(self, attr):      
          
        if self._languageversion is None:
            return 'Unknown case' if attr == 'CaseNumber' else None

        if attr in BibliographyLanguageVersionModel.FieldNames:
            setattr(self, attr, getattr(self._languageversion, attr))
            return getattr(self, attr)

        for part in [BibliographyBaseModel, TextModel, CitationSupplementModel]:
            if attr in getattr(part, 'FieldNames'):
                model = getattr(self._languageversion, DecisionProxy.__map[part])
                for field in getattr(part, 'FieldNames'):
                    setattr(self, field, getattr(model, field))
                    if field in DecisionProxy.__splitFields:
                        splitversion = [x for x in getattr(self, field).split(',') if x != '']
                        setattr(self, field, splitversion)
                return getattr(self, attr)
    

    def __str__(self):
        return 'DecisionProxy: {}  {} {}.'.format(self.CaseNumber, self.DecisionDate, self.DecisionLanguage)
    


    @property
    def AllGoodCited(self):
        goodBibCited = {x for x in self.CitedCases.split(',') if x not in self.CitedCases_notInDB.split(',')}
        goodTextCited = {x for x in self.TextCited_inDB.split(',') if x != ''}
        allGood = set.union(goodBibCited, goodTextCited)
        return allGood
        
    @property
    def AllCiting(self):
        bibCiting = {x for x in self.BibliographyCiting.split(',') if x !=''}
        textCiting = {x for x in self.TextCiting.split(',') if x != ''}
        allCiting = set.union(bibCiting, textCiting)
        return allCiting
        