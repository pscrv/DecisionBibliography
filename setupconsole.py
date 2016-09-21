"""
Python module to initialse the python interactive environment
"""


import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DecisionBibliography.settings')
import django
django.setup()
from app.models import DecisionBibliographyModel as db


def Setup():
   pass