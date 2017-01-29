from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Checks whether all cases in the CitedCases field appear in the DB'
    # See https://docs.djangoproject.com/en/1.9/howto/custom-management-commands/#module-django.core.management

    
    def handle(self, *args, **options):
        import textwrap
        from Decisions.management.utilities import DBInspector        

        cited = DBInspector.FindCitedCaseNumbers()
        citedNotInDB = DBInspector.FindCitedCasesNotInDB()            
        citedGroupedByType = {type: [x for x in citedNotInDB if x[0] == type] for type in DBInspector.DECISIONTYPELETTERS}

        self.stdout.write('Number of distinct case numbers cited: {}'.format(len(cited)))
        self.stdout.write('Cited case numbers not in DB: {}'.format(len(citedNotInDB)))

        for type, count in citedGroupedByType.items():
            self.stdout.write(
                textwrap.shorten(
                    'Type {}: {} --- {}'.format(
                        type, 
                        len(citedGroupedByType[type]), 
                        citedGroupedByType[type], 100
                        ), 
                    100
                    ))
        
         







