from django.core.management.base import BaseCommand
from Decisions.management.utilities import DBInspector
from Decisions.models import DecisionBibliographyModel

# See https://docs.djangoproject.com/en/1.9/howto/custom-management-commands/#module-django.core.management
class Command(BaseCommand):
    help = 'Counts decisions of different types'

    
    def handle(self, *args, **options):

        citedNotInDB = DBInspector.FindCitedCasesNotInDB()
        self.stdout.write('{} cases are cited, but are not in the DB.'.format(len(citedNotInDB)))

        citingdecisions = {}
        for cited in citedNotInDB:
            citingcases = DecisionBibliographyModel.objects.FilterOnlyPrLanguage(CitedCases__contains=cited).all()
            citingdecisions[cited] = set(x.CaseNumber for x in citingcases)

        self.stdout.write('Results:')
        for cited in citingdecisions:
            self.stdout.write('{} --> {}'.format(cited, str(citingdecisions[cited])))




        