"""
Definition of urls for DecisionBibliography.
"""

from django.conf.urls import url, include

# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [ 
    # TO DO: remove the next line when DecsionAnalyser is not being tested
    #url(r'^$', include('DecisionAnalyser.urls')),
    
    url(r'^DecisionAnalyser/', include('DecisionAnalyser.urls')),
    url(r'', include('app.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
]
