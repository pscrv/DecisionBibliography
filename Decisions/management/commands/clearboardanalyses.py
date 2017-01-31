from django.core.management.base import BaseCommand

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        from Decisions.models import BoardAnalysisModel
        
        startcount = BoardAnalysisModel.objects.count()

        self.stdout.write('Trying to delete {} records from {}'.format(startcount, BoardAnalysisModel))
        BoardAnalysisModel.objects.all().delete()
        endcount = BoardAnalysisModel.objects.count()
        self.stdout.write('Deleted {} records.'.format(startcount - endcount))



                        

