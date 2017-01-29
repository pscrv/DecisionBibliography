from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Populates the DB for one board'
    # See https://docs.djangoproject.com/en/1.9/howto/custom-management-commands/#module-django.core.management

    #def add_arguments(self, parser):
    #    parser.add_argument('board', type=str)

    def handle(self, *args, **options):

        from Decisions.models import DecisionBibliographyModel
        startcount = DecisionBibliographyModel.objects.count()
        self.stdout.write('DB contains ' + str(startcount) + ' records.')
        self.stdout.write('Populating...')


        from Decisions.management.utilities.DBPopulator import BibliographyGetter
        populator = BibliographyGetter()
        typestartcount = startcount
        #for casetype in 'DGRW':
        #    self.stdout.write('Getting type {}.'.format(casetype))
        #    populator.GetAllForType(casetype)
        #    typeendcount = DecisionBibliographyModel.objects.count()
        #    self.stdout.write('{} decisions added.'.format(str(typeendcount - typestartcount)))
        #    typestartcount = typeendcount

        self.stdout.write('Getting J and T decisions')
        boardlist = [
            '3.1.01',
            '3.2.01', '3.2.02', '3.2.03', '3.2.04', '3.2.05', '3.2.06', '3.2.07', '3.2.08',
            '3.3.01', '3.3.02', '3.3.03', '3.3.04', '3.3.05', '3.3.06', '3.3.07', '3.3.08', '3.3.09', '3.3.10', 
            '3.4.01', '3.4.02', '3.4.03', 
            '3.5.01', '3.5.02', '3.5.03', '3.5.04', '3.5.05', '3.5.06', '3.5.07']
        
        boardstartcount = DecisionBibliographyModel.objects.count()
        for board in boardlist:
            self.stdout.write('Adding board {}'.format(board))
            populator.GetAllForBoard(board)
            boardendcount = DecisionBibliographyModel.objects.count()
            self.stdout.write('{} decisions added.'.format(str(boardendcount - boardstartcount)))
            boardstartcount = boardendcount
        
        endcount = DecisionBibliographyModel.objects.count()
        self.stdout.write('\nDB contains ' + str(endcount) + ' records.')
        self.stdout.write('{} records have been added altoghether.'.format(str(endcount - startcount)))
