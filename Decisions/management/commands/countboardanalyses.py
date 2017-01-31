from django.core.management.base import BaseCommand

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        from Decisions.models import BoardAnalysisModel
        
        self.stdout.write('BoardAnalyses: {}.'.format(BoardAnalysisModel.objects.count()))



                        

