import django
from django.test import TestCase

class Anything(TestCase):

    if django.VERSION[:2] >= (1, 7):
        # Django 1.7 requires an explicit setup() when running tests in PTVS
        @classmethod
        def setUpClass(cls):
            super().setUpClass()
            django.setup()


    def test_anything(self):

        from DecisionsPlus.management.commands import copyBib_fromDecisionsDB
        command = copyBib_fromDecisionsDB.Command()
        command.handle()
        
        x = 1