from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.template import RequestContext
from DecisionAnalyser.ViewModels.Tryout import TryoutViewModel


def home(request):    
    """Renders the home page."""
    assert isinstance(request, HttpRequest)

    from DecisionAnalyser.DecisionProvider import SimpleDecisionProvider
    provider = SimpleDecisionProvider()
    decisions = provider.GetDecisions('restitutio')

    viewModel = TryoutViewModel(decisions)
    return render(
        request,
        'DecisionAnalyser/index.html',
        viewModel.Context,
    )

      
