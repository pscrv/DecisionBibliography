from django.core.management.base import BaseCommand

from Decisions.models import DecisionBibliographyModel, DecisionSupplementaryModel
from Decisions.management.supplements.utilities import SupplementManager


class Command(BaseCommand):

    def __init__(self):
        super().__init__()
        self.__allCaseNumbers = DecisionBibliographyModel.objects.values_list('CaseNumber', flat = True)
        self.__bibliographies = DecisionBibliographyModel.objects.exclude(TextModel = None)
        self.__supplementManager = SupplementManager()


    def handle(self, *args, **options):

        startcount = DecisionSupplementaryModel.objects.count()
        self.stdout.write('Making supplements and adding fields for cited cases.')
        self.stdout.write('  {} case numbers in the database.'.format(len(self.__allCaseNumbers)))
        self.stdout.write('  Making supplements for {} cases with texts.'.format(self.__bibliographies.count()))
        self.stdout.write('  {} supplements currently in the database'.format(startcount))


        index = 0
        for bibliography in self.__bibliographies:
            self.__supplementManager.AddCited(bibliography)
            index += 1
            if index % 100 == 0:
                self.stdout.write('  processing case {} <{}>'.format(index, bibliography))

        endcount = DecisionSupplementaryModel.objects.count()
        self.stdout.write('{} supplements now in the database ({} added).'.format(endcount, endcount - startcount))
                        

