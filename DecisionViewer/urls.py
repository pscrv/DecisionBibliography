"""
Definition of urls for DecisionBibliography.
"""

from django.conf.urls import url
from django.contrib.auth.views import login, logout

from datetime import datetime
from DecisionViewer import views


urlpatterns = [ 
    url(r'^$', views.home, name='home'),
    url(r'^decisionFromCaseNumber/(?P<cn>.+)/$', views.decisionFromCaseNumber, name='decision'),
    url(r'^decision/(?P<pk>\d+)/$', views.decision, name='decision'),
    url(r'^decision/(?P<pk>\d+)(?P<highlightterms>.+)/$', views.decision, name='decision_with_highlight'),
    url(r'^search/$', views.search, name='search'),
    url(r'^boardtimelines/$', views.boardtimelines, name='boardtimelines'),
    url(r'^board/(?P<bd>.+)/$', views.board, name='board'),
    url(r'^about', views.about, name = 'about'),
    url(r'^textsearch', views.textsearch, name = 'textsearch'),
]
