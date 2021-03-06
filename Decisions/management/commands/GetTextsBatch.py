from django.core.management.base import BaseCommand

from datetime import datetime

from Decisions.models import DecisionBibliographyModel, DecisionTextModel
from Decisions.DBHelpers.TextHelpers import TextGetter

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        
        HOWMANY = 1
        textgetter = TextGetter()

        starttextcount = DecisionTextModel.objects.count()
        self.stdout.write('DB has {} texts.'.format(starttextcount))
        self.stdout.write('Getting texts ...\n')

        count = 0
        starttime = datetime.now()
        currenttime = starttime
        for bibliography in DecisionBibliographyModel.objects.filter(TextModel = None)[:HOWMANY]:
            
            text = textgetter.Get_Text(bibliography)
            text_ok = text.Facts != '' or text.Reasons != '' or text.Order != ''
            if text_ok:
                self.stdout.write('     >>> Added {} (bibliography: {}).'.format(text, bibliography))
                #bibliography.TextModel = text
            else:
                text.delete()
                self.stdout.write('      >>> Could not find text for {}'.format(bibliography))

            count += 1
            if count >= HOWMANY:
                endtime = datetime.now()
                delta = (endtime - starttime).seconds
                endtextcount = DecisionTextModel.objects.count()
                self.stdout.write('Done. DB now contains {} texts.)'.format(endtextcount))
                self.stdout.write('   {} texts added in {} seconds'.format(endtextcount - starttextcount, delta))
                return
            if count % 10 == 0:
                newtime = datetime.now()
                delta = (newtime - currenttime).seconds
                currenttime = newtime
                self.stdout.write('  {} so far ... ({} seconds)'.format(count, delta))


        self.stdout.write('\n Reach the end of the databse.')



                        

