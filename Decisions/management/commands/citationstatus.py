from django.core.management.base import BaseCommand

import re

from Decisions import Formatters

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        from Decisions.management.utilities import TextDBInspector      

        status = TextDBInspector.GetCitationStatus()

        self.stdout.write('Done.\n')
        self.stdout.write('\n  {} decision texts in DB'.format(status['textcount']))
        self.stdout.write('\n  {} cases have extra citations:'.format(len(status['extra'])))
        #for case in extra:
        #    self.stdout.write('{} >>> {}'.format(case, extra[case]))
        self.stdout.write('\n  {} cases have missing citations:'.format(len(status['missing'])))
        #for case in missing:
        #    self.stdout.write('{} >>> {}'.format(case, missing[case]))
        self.stdout.write('\n  {} cases have bad citations:'.format(len(status['bad'])))
        #for case in bad:
        #    self.stdout.write('{} >>> {}'.format(case, bad[case]))

 


                        

