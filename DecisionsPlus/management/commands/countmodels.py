from django.core.management.base import BaseCommand

from DecisionsPlus.models import BibliographyBaseModel 
from DecisionsPlus.management.utilities import _inspector

class Command(BaseCommand):
    
    def handle(self, *args, **options):

        self.stdout.write('Model counts:')
        self.__writecounts(_inspector.GetModelCounts())
    
    def __writecounts(self, counts):        
        for key,value in counts.items():
            self.stdout.write('    {}: {}'.format(key, value))