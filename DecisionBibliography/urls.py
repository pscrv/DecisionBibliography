"""
Definition of urls for DecisionBibliography.
"""

from django.conf.urls import url, include

urlpatterns = [     
    url(r'', include('DecisionViewer.urls')),
]
