"""
Unit tests
"""

import django
from django.test import TestCase


class test_BoardGrouping(TestCase):
    
    @classmethod
    def setUpClass(cls):    
        super(test_BoardGrouping, cls).setUpClass()
        django.setup()
    
    def test_boardGrouper(self):
        from ViewModels import IndexVM
        vm = IndexVM.IndexViewModel()
        self.assertEqual(vm.Context['boards'][6], ('EBA',  ['EBA']))
        self.assertEqual(vm.Context['boards'][0], ('3.1',  ['3.1.01']))
  