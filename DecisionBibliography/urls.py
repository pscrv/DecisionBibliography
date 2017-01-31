"""
Definition of urls for DecisionBibliography.
"""

from django.conf.urls import url, include

urlpatterns = [     
    url(r'^DecisionAnalyser/', include('DecisionAnalyser.urls')),
    url(r'', include('Decisions.urls')),
]
