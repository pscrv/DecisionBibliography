"""
Definition of urls for DecisionBibliography.
"""

from datetime import datetime
from django.conf.urls import url
from django.contrib.auth.views import login, logout
from app.forms import BootstrapAuthenticationForm
from app import views

# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()


urlpatterns = [ 
    url(r'^$', views.home, name='home'),
    url(r'^decisionFromCaseNumber/(?P<cn>.+)/$', views.decisionFromCaseNumber, name='decision'),
    url(r'^decision/(?P<pk>\d+)(?P<highlightterms>.+)/$', views.decision, name='decision_with_highlight'),
    url(r'^decision/(?P<pk>.+)/$', views.decision, name='decision'),
    url(r'^search', views.search, name='search'),
    url(r'^boardtimelines/$', views.boardtimelines, name='boardtimelines'),
    url(r'^board/(?P<bd>.+)/$', views.board, name='board'),
    url(r'^about', views.about, name = 'about'),
    url(r'^textsearch', views.textsearch, name = 'textsearch'),

    
    url(r'^login/$',
        login,
        {
            'template_name': 'app/login.html',
            'authentication_form': BootstrapAuthenticationForm,
            'extra_context':
            {
                'title':'Log in',
                'year':datetime.now().year,
            }
        },
        name='login'),

    url(r'^logout$',
        logout,
        {
            'next_page': '/',
        },
        name='logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
]
#urlpatterns = patterns('',
#    # Examples:
#    url(r'^$', 'app.views.home', name='home'),
#    url(r'^contact$', 'app.views.contact', name='contact'),
#    url(r'^about', 'app.views.about', name='about'),
#    url(r'^login/$',
#        'django.contrib.auth.views.login',
#        {
#            'template_name': 'app/login.html',
#            'authentication_form': BootstrapAuthenticationForm,
#            'extra_context':
#            {
#                'title':'Log in',
#                'year':datetime.now().year,
#            }
#        },
#        name='login'),
#    url(r'^logout$',
#        'django.contrib.auth.views.logout',
#        {
#            'next_page': '/',
#        },
#        name='logout'),

#    # Uncomment the admin/doc line below to enable admin documentation:
#    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

#    # Uncomment the next line to enable the admin:
#    # url(r'^admin/', include(admin.site.urls)),
#)
