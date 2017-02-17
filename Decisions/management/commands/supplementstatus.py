from django.core.management.base import BaseCommand

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        from Decisions.management.utilities import SupplementDBInspector      

        status = SupplementDBInspector.count()
        self.stdout.write('{} supplements in DB.'.format(status))

 


                        

