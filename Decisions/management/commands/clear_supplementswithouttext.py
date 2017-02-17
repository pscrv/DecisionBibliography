from django.core.management.base import BaseCommand


class Command(BaseCommand):
    
    def handle(self, *args, **options):
        from Decisions.models import DecisionBibliographyModel, DecisionTextModel, DecisionSupplementaryModel

        startcount = DecisionSupplementaryModel.objects.count()
        self.stdout.write('Deleting all SupplementModels that have no TextModel.')
        self.stdout.write('  Starting with {} supplements'.format(startcount))
    
        todelete = DecisionBibliographyModel.objects.exclude(SupplementModel = None).filter(TextModel = None)
        todelete.delete()
                
        endcount = DecisionSupplementaryModel.objects.count()
        self.stdout.write('Done.')
        self.stdout.write('  Ending with {} records.'.format(endcount))

