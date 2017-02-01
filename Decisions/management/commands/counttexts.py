from django.core.management.base import BaseCommand

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        from Decisions.models import DecisionTextModel
        
        self.stdout.write('BoardAnalyses: {}.'.format(DecisionTextModel.objects.count()))
        for x in DecisionTextModel.objects.all():
            self.stdout.write(str(x))



                        

