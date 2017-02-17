from django.core.management.base import BaseCommand

import re

from Decisions import Formatters

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        from Decisions.models import DecisionBibliographyModel, DecisionTextModel, DecisionSupplementaryModel

        startcount = DecisionTextModel.objects.count()
        self.stdout.write('Deleting empty supplement models')
        self.stdout.write('  Starting with {} records'.format(startcount))
    
        supplements = DecisionTextModel.objects.filter(Facts = '', Reasons = '', Order = '')
        supplements.delete()

                
        endcount = DecisionTextModel.objects.count()
        self.stdout.write('Done.')
        self.stdout.write('  Ending with {} records.'.format(endcount))



                        

