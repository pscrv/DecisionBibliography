from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.template import RequestContext

from DecisionAnalyser.ViewModels.AnalysedDecision import AnalysedDecisionViewModel




def analysed_decision(request, pk, analysername="restitutio"):
    assert isinstance(request, HttpRequest)

    from app.DBProxy import DecisionModelProxy
    decision = DecisionModelProxy.GetDecisionFromPrimaryKey(pk)

    viewModel = AnalysedDecisionViewModel(decision, analysername)
    
    return render(
        request,
        'DecisionAnalyser/analyseddecision.html',
        viewModel.Context,
        )
      
