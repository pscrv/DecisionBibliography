from django.core.management.base import BaseCommand
from Decisions.management.utilities import DBInspector
#from app.models import DecisionBibliographyModel

# See https://docs.djangoproject.com/en/1.9/howto/custom-management-commands/#module-django.core.management
class Command(BaseCommand):
    help = 'Counts decisions of different types'

    
    def handle(self, *args, **options):

        self.stdout.write('Total decisions: {} (unique case numbers: {})'.format(
            DBInspector.CountRecords(),
            DBInspector.CountCaseNumbers()
            ))

        types = 'DGJRTW'
        for t in types:
            self.stdout.write('Type {}: {} (unique case numbers: {})'.format(
                t, 
                DBInspector.CountDecisionType(t), 
                DBInspector.CountCaseNumbersForType(t)
                ))



        