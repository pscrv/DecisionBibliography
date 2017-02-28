from django.core.management.base import BaseCommand

from datetime import datetime
from Decisions.models import DecisionBibliographyModel
from DecisionsPlus.models import BibliographyBaseModel,  BibliographyLanguageVersionModel, TextModel, CitationSupplementModel
from DecisionsPlus.management.utilities import _textsupps

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        LIMIT = None
        GROUPSIZE = 10


        startcount = BibliographyBaseModel.objects.count()
        self.stdout.write('Starting with {} entries.'.format(startcount))
        old_bibs = DecisionBibliographyModel.objects.exclude(TextModel = None)[:LIMIT]        
        #old_bibs = DecisionBibliographyModel.objects.all()[:LIMIT]
        self.stdout.write('Copying {} entries.'.format(old_bibs.count()))
                
        count = 0
        groupstarttime = datetime.now()
        starttime = datetime.now()        
        for bib in old_bibs:

            try:
                newbase = BibliographyBaseModel.objects.get(CaseNumber = bib.CaseNumber, DecisionDate = bib.DecisionDate)
                for field in BibliographyBaseModel.FieldNames:
                    setattr(newbase, field, getattr(bib, field))
            except BibliographyBaseModel.DoesNotExist:
                basedict = {f: getattr(bib, f) for f in BibliographyBaseModel.FieldNames}
                newbase = BibliographyBaseModel(**basedict)

            cited = [x.strip() for x in newbase.CitedCases.split(',') if x != '']
            newbase.CitedCases = ','.join(cited)
            newbase.save()


            try:
                newlang = BibliographyLanguageVersionModel.objects.get(BibliographyBase = newbase, DecisionLanguage = bib.DecisionLanguage)
                for field in BibliographyBaseModel.FieldNames:
                    setattr(newlang, field, getattr(bib, field))
            except BibliographyLanguageVersionModel.DoesNotExist:
                langdict = {f: getattr(bib, f) for f in BibliographyLanguageVersionModel.FieldNames}
                langdict['BibliographyBase'] = newbase
                newlang = BibliographyLanguageVersionModel(**langdict)
            newlang.save()
               
            count += 1
            if count % GROUPSIZE == 0:
                groupendtime = datetime.now()
                self.stdout.write(' ... latest save: {}.'.format(bib))
                self.stdout.write('   as ({} ### {}).'.format(newbase, newlang))
                self.stdout.write('   {} so far.'.format(count))
                self.stdout.write('     last {} in {} seconds'.format(GROUPSIZE, (groupendtime - groupstarttime).seconds))
                groupstarttime = datetime.now()
            
    
        endtime = datetime.now()
        self.stdout.write('Done.')
        self.stdout.write('  There are now {} entries.'.format(BibliographyBaseModel.objects.count()))
        self.stdout.write('      {} seconds total'.format((endtime - starttime).seconds))