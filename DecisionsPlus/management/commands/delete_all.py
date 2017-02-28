from django.core.management.base import BaseCommand

from DecisionsPlus.models import BibliographyBaseModel 
from DecisionsPlus.management.utilities import _inspector

class Command(BaseCommand):
    
    def handle(self, *args, **options):

        self.stdout.write('Deleting all entries.')
        self.stdout.write('  Starting with: ')
        self.__writecounts(_inspector.GetModelCounts())
    
        from DecisionsPlus.models import BibliographyLanguageVersionModel
        #todelete = BibliographyLanguageVersionModel.objects.exclude(TextModel = None)
        #self.stdout.write('  Deleting {} records'.format(todelete.count()))
        #todelete = BibliographyBaseModel.objects.all()
        #todelete.delete()
                
        self.stdout.write('Done.')
        self.__writecounts(_inspector.GetModelCounts())
        

    def __writecounts(self, counts):        
        for key,value in counts.items():
            self.stdout.write('    {}: {}'.format(key, value))