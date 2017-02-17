from django.core.management.base import BaseCommand

from datetime import datetime

from Decisions.models import DecisionBibliographyModel, DecisionTextModel
from Decisions.DBHelpers.TextHelpers import TextGetter
from Decisions.management.supplements.utilities import SupplementManager

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        
        howmany = 100
        textgetter = TextGetter()
        supplementManager = SupplementManager()
        starttime = datetime.now()
        starttextcount = DecisionTextModel.objects.count()


        self.stdout.write('DB has {} texts.'.format(starttextcount))
        self.stdout.write('Getting texts ...\n')

        count = 0
        currenttime = starttime
        #for bibliography in DecisionBibliographyModel.objects.all():
        for bibliography in DecisionBibliographyModel.objects.filter(TextModel = None)[:howmany]:
            
            #try:
            #    text = DecisionTextModel.objects.get(Bibliography = bibliography)
            #    continue
            #except Exception as ex:
                text = textgetter.Get_Text(bibliography)
                text_ok = text.Facts != '' or text.Reasons != '' or text.Order != ''
                if text_ok:
                    self.stdout.write('     >>> Added {} (bibliography: {}).'.format(text, bibliography))
                    bibliography.TextModel = text
                    supplementManager.AddCited(bibliography)
                    supplementManager.AddCiting(bibliography)
                else:
                    self.stdout.write('      >>> Could not find text for {}'.format(bibliography))

                count += 1
                if count >= howmany:
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



                        

