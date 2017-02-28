from django.core.management.base import BaseCommand

from DecisionsPlus.models import TextModel, CitationSupplementModel 
from DecisionsPlus.management.utilities import _inspector

class Command(BaseCommand):
    
    def handle(self, *args, **options):

        self.stdout.write('Deleting all texts and supplements.')
        self.stdout.write('  Starting with: ')
        self.__writecounts(_inspector.GetModelCounts())
    
        todelete = TextModel.objects.all()
        todelete.delete()
        
        todelete = CitationSupplementModel.objects.all()
        todelete.delete()
                
        self.stdout.write('Done.')
        self.__writecounts(_inspector.GetModelCounts())
        

    def __writecounts(self, counts):        
        for key,value in counts.items():
            self.stdout.write('    {}: {}'.format(key, value))