from django.core.management.base import BaseCommand

from datetime import datetime
from DecisionsPlus.models import BibliographyBaseModel

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        LIMIT = None
        GROUPSIZE = 10


        startcount = BibliographyBaseModel.objects.count()
        self.stdout.write('Starting with {} entries.'.format(startcount))
        bibs = BibliographyBaseModel.objects.all()[:LIMIT]
        self.stdout.write('Cleaning {} entries.'.format(bibs.count()))
                
        count = 0
        groupstarttime = datetime.now()
        starttime = datetime.now()        
        for bib in bibs:
            count += 1
            if bib.CitedCases == '': 
                continue
            
            cited = [x.strip() for x in bib.CitedCases.split(',') if x != '']
            bib.CitedCases = ','.join(cited)
            bib.save()            
               
            if count % GROUPSIZE == 0:
                groupendtime = datetime.now()
                self.stdout.write(' ... latest cleaned: {}.'.format(bib))
                self.stdout.write('   {} so far.'.format(count))
                self.stdout.write('     last {} in {} seconds'.format(GROUPSIZE, (groupendtime - groupstarttime).seconds))
                groupstarttime = datetime.now()
            
    
        endtime = datetime.now()
        self.stdout.write('Done.')
        self.stdout.write('  There are now {} entries.'.format(BibliographyBaseModel.objects.count()))
        self.stdout.write('      {} seconds total'.format((endtime - starttime).seconds))