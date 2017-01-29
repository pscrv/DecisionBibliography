from django.core.management.base import BaseCommand

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        from Decisions.EpoSearchFacade import EpoSearchFacade
        from Decisions.EpoConverter import EpoConverter
        from Decisions.models import DecisionBibliographyModel

        searcher = EpoSearchFacade()
        converter = EpoConverter()

        board = '3.3.04'
        yeardigitpair = '08'

        try:
            response = searcher.SearchByBoardAndCaseYear(board, yeardigitpair)
            decs = converter.ResponseToDecisionList(response)
        except Exception as ex:
            t = type(ex)
            return

        self.stdout.write('Extracted {} records'.format(len(decs)))

        failurecount = 0
        for case in decs:
            inDB = DecisionBibliographyModel.objects.filter(
                CaseNumber = case.CaseNumber,
                ).first()

            if not inDB:
                self.stdout.write('{} is not in the DB.'.format(case.CaseNumber))
                failurecount += 1
            
        self.stdout.write('{} cases failed.'.format(failurecount))



                        

