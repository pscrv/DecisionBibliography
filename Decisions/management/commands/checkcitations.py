from django.core.management.base import BaseCommand

from Decisions import Formatters

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        from Decisions.management.utilities import BibliographyBibliographyDBInspector

        missing = BibliographyDBInspector.FindMissingCitations()

        self.stdout.write('{} problematic cases found.'.format(len(missing)))

        for case in missing:
            self.stdout.write('   {} >>> {}'.format(case, missing[case]))

                        

