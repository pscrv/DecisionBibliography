from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.template import RequestContext

from Decisions import Formatters
from Decisions.DBProxy import DecisionModelProxy

from Decisions.ViewModels import BoardVM
from Decisions.ViewModels import DbStateVM
from Decisions.ViewModels import DecisionVM 
from Decisions.ViewModels import TimeLinesVM 
from Decisions.ViewModels import BoardVM 
from Decisions.ViewModels import IndexVM
from Decisions.ViewModels import TextSearchVM


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)

    viewModel = IndexVM.IndexViewModel()
    return render(
        request,
        'Decisions/index.html',
        viewModel.Context,
    )

      

def decision(request, pk, highlightterms = '[]'):
    """Renders a single decision."""
    assert isinstance(request, HttpRequest)
    from ast import literal_eval

    decision = DecisionModelProxy.GetDecisionFromPrimaryKey(pk)
    decisions = DecisionModelProxy.GetListFromCaseNumber(decision.CaseNumber)
    hlterms = literal_eval(highlightterms)
    viewModel = DecisionVM.DecisionViewModel(decisions, pk=pk, highlightterms=hlterms)
    return render(
        request,
        'Decisions/decision.html',
        viewModel.Context,
    ) 

def decisionFromCaseNumber(request, cn):
    """Renders a single decision."""
    assert isinstance(request, HttpRequest)

    caseNumber = Formatters.formatCaseNumber(cn)
    decisions = DecisionModelProxy.GetListFromCaseNumber(caseNumber)
    viewModel = DecisionVM.DecisionViewModel(decisions)
    return render(
        request,
        'Decisions/decision.html',
        viewModel.Context,
    ) 

def search(request):
    if not request.method == 'POST':
        return redirect(request.META['HTTP_REFERER'])
        
    query = request.POST.get('q', None)
    return redirect (decisionFromCaseNumber, query)

def boardtimelines(request):
    """Renders a view of board timelines."""
    assert isinstance(request, HttpRequest)

    viewModel = TimeLinesVM.TimeLinesViewModel()
    return render(
        request,
        'Decisions/boardtimelines.html',
        viewModel.Context,
        )        

def board(request, bd):
    """Renders a view of board information."""
    assert isinstance(request, HttpRequest)
    viewModel = BoardVM.BoardViewModel(bd)
    return render(
        request,
        'Decisions/board.html',
        viewModel.Context,
        )

def about(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    
    viewModel = DbStateVM.DbStateViewModel()
    return render(
        request,
        'Decisions/about.html',
        viewModel.Context,
    )

def textsearch(request):
    """Renders the text search page."""
    assert isinstance(request, HttpRequest)

    if request.method == 'POST':
        query = request.POST.get('q', '')
    else:
        query = ''

    viewModel = TextSearchVM.TextSearchViewModel(query)
    return render(
        request,
        'Decisions/textsearch.html',
        viewModel.Context
    )






