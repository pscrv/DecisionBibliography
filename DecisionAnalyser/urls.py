from django.conf.urls import url
from  DecisionAnalyser import views


urlpatterns = [
    
    url(r'^(?P<pk>.+)/(?P<analysername>.+)/$', views.analysed_decision, name = 'DecisionAnalyser'),
    url(r'^(?P<pk>.+)/$', views.analysed_decision, name = 'DecisionAnalyser'),   
    
    ]
