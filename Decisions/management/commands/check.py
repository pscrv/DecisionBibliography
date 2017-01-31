from django.core.management.base import BaseCommand

from Decisions.management.utilities import DBInspector   
from Decisions.EpoSearchFacade import EpoSearchFacade
from Decisions.EpoConverter import EpoConverter
from Decisions.models import DecisionBibliographyModel

class Command(BaseCommand):
    help = 'Checks whether all cases in the CitedCases field appear in the DB; tries to obtain those that are missing.'
    # See https://docs.djangoproject.com/en/1.9/howto/custom-management-commands/#module-django.core.management

    
    def handle(self, *args, **options):
        import textwrap     

        cited = DBInspector.FindCitedCaseNumbers()
        citedNotInDB = DBInspector.FindCitedCasesNotInDB()            
        citedGroupedByType = {type: [x for x in citedNotInDB if x[0] == type] for type in DBInspector.DECISIONTYPELETTERS}
        
        self.stdout.write('Number of distinct case numbers cited: {}'.format(len(cited)))
        self.stdout.write('Cited case numbers not in DB: {}'.format(len(citedNotInDB)))
        self.stdout.write('Looking for missing case number online')

        searcher = EpoSearchFacade()
        convertor = EpoConverter()
        foundonline = []
        foundonlinecount = 0
        notfoundonline = []
        for notfoundcase in citedNotInDB:
            self.stdout.write('... {} ...'.format(notfoundcase))
            found = searcher.SearchCaseNumber(notfoundcase)
            if found:
                foundonline += convertor.ResponseToDecisionList(found)
                foundonlinecount += 1
            else:
                notfoundonline.append(notfoundcase)
                        
        self.stdout.write('\n')
        self.stdout.write('Found {} case numbers online, {} decisions'.format(foundonlinecount, len(foundonline)))

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

        if foundonlinecount > 0:
            self.stdout.write('Writing found cases do DB ...')
            start = DecisionBibliographyModel.objects.count()
            for found in foundonline:
                found.save()
            end = DecisionBibliographyModel.objects.count()
            self.stdout.write('{} decisions added.'.format(end - start))








