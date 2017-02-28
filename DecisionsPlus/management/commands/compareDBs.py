from django.core.management.base import BaseCommand

from Decisions.models import DecisionBibliographyModel
from DecisionsPlus.models import BibliographyBaseModel,  BibliographyLanguageVersionModel, TextModel, CitationSupplementModel


class Command(BaseCommand):
    
    def handle(self, *args, **options):

        DcsnDB_cns = DecisionBibliographyModel.objects.values_list('CaseNumber', flat = True).distinct()
        DplusDB_cns = BibliographyBaseModel.objects.values_list('CaseNumber', flat = True).distinct()

        self.stdout.write('DecisionBibliographyModel: {} distinct case nubmbers.'.format(DcsnDB_cns.count()))
        self.stdout.write('BibliographyBaseModel: {} distinct case nubmbers.'.format(DplusDB_cns.count()))