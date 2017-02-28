from django.core.management.base import BaseCommand

from datetime import datetime
from Decisions.models import DecisionBibliographyModel
from DecisionsPlus.models import BibliographyBaseModel,  BibliographyLanguageVersionModel, TextModel, CitationSupplementModel
from DecisionsPlus.management.utilities import _textsupps

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        LIMIT = None
        GROUPSIZE = 50


        startcount = BibliographyBaseModel.objects.count()
        self.stdout.write('Starting with {} entries.'.format(startcount))
        old_bibs = DecisionBibliographyModel.objects.exclude(TextModel = None)[:LIMIT]
        self.stdout.write('Copying {} entries.'.format(old_bibs.count()))
                
        count = 0
        groupstarttime = datetime.now()
        starttime = datetime.now()        
        for bib in old_bibs:

            languageModels = BibliographyLanguageVersionModel.objects.filter(
                BibliographyBase__CaseNumber = bib.CaseNumber,
                BibliographyBase__DecisionDate = bib.DecisionDate,
                DecisionLanguage = bib.DecisionLanguage)

            languageModel = languageModels.first()
            if len(languageModels) > 1:
                languageModels[1:].delete()


            if hasattr(languageModel, 'TextModel'):
                languageModel.TextModel.delete()
                
            if hasattr(languageModel, 'CitationSupplementModel'):
                languageModel.CitationSupplementModel.delete()
            
            if hasattr(bib, 'TextModel'):
                textdict = {f: getattr(bib.TextModel, f) for f in TextModel.FieldNames}
                text = TextModel(**textdict)
                text.Bibliography = languageModel
                text.save()                
                _textsupps.AddSupp(languageModel)                
   
            count += 1
            if count % GROUPSIZE == 0:
                groupendtime = datetime.now()
                self.stdout.write(' ... latest save: {}.'.format(bib))
                self.stdout.write('   under {}).'.format(languageModel))
                self.stdout.write('   {} so far.'.format(count))
                self.stdout.write('     last {} in {} seconds'.format(GROUPSIZE, (groupendtime - groupstarttime).seconds))
                groupstarttime = datetime.now()
            
    
        endtime = datetime.now()
        self.stdout.write('Done.')
        self.stdout.write('  There are now {} entries.'.format(BibliographyBaseModel.objects.count()))
        self.stdout.write('      {} seconds total'.format((endtime - starttime).seconds))