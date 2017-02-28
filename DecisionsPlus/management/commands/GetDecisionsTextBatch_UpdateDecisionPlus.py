from django.core.management.base import BaseCommand

from datetime import datetime

from Decisions.models import DecisionBibliographyModel, DecisionTextModel
from Decisions.DBHelpers.TextHelpers import TextGetter
from DecisionsPlus.management.utilities import _textsupps
from DecisionsPlus.models import TextModel

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        
        HOWMANY = 100
        textgetter = TextGetter()

        DBstarttextcount = DecisionTextModel.objects.count()
        Plusstarttextcount = TextModel.objects.count()
        self.stdout.write('DB has {} texts.'.format(DBstarttextcount))
        self.stdout.write('DBPlus has {} texts.'.format(Plusstarttextcount))
        self.stdout.write('Getting texts ...\n')

        count = 0
        starttime = datetime.now()
        currenttime = starttime
        for bibliography in DecisionBibliographyModel.objects.filter(TextModel = None)[:HOWMANY]:
            
            text = textgetter.Get_Text(bibliography)
            text_ok = text.Facts != '' or text.Reasons != '' or text.Order != ''
            if text_ok:
                _textsupps.AddDecisionPlusTextAndSuppFromDecisionsDB(bibliography)
                self.stdout.write('     >>> Added {} to DB (bibliography: {}).'.format(text, bibliography))
            else:
                text.delete()
                self.stdout.write('      >>> Could not find text for {}'.format(bibliography))

            count += 1
            if count >= HOWMANY:
                endtime = datetime.now()
                delta = (endtime - starttime).seconds
                DBendtextcount = DecisionTextModel.objects.count()
                Plusendtextcount = DecisionTextModel.objects.count()
                self.stdout.write('Done. DB now contains {} texts.)'.format(DBendtextcount))
                self.stdout.write('Done. DBPlus now contains {} texts.)'.format(Plusendtextcount))
                self.stdout.write('   {} texts added in {} seconds'.format(DBendtextcount - DBstarttextcount, delta))
                return
            if count % 10 == 0:
                newtime = datetime.now()
                delta = (newtime - currenttime).seconds
                currenttime = newtime
                self.stdout.write('  {} so far ... ({} seconds)'.format(count, delta))


        self.stdout.write('\n Reach the end of the databse.')



                        

