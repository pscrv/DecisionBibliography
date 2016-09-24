"""
Definition of views.
"""

from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.template import RequestContext

from . models import DecisionBibliographyModel
from ViewModels import BoardVM
from ViewModels import DbStateVM
from ViewModels import DecisionVM 
from ViewModels import TimeLinesVM 
from ViewModels import BoardVM 


def home(request):

    #region experiement
    #from . import DBAnalyser
    #analyser = DBAnalyser.ProvisionAnalyser()
    #x = analyser.ArticleFrequencyForBoard('3.5.01')
    #y = analyser.RuleFrequencyForBoard('3.5.01')
    #z = 1
    #endregion

    # region comment out this, if db is not being populated
    #start = datetime(1990, 1, 1)
    #end = datetime(1999, 12, 31)

    #from . GetDecisionBibliographies import BibliographyGetter
    #bg = BibliographyGetter()
    #bg.Get_FromDate_ToDate(start, end) 
    # endregion

    """Renders the home page."""
    assert isinstance(request, HttpRequest)

    viewModel = DbStateVM.DbStateViewModel()
    return render(
        request,
        'app/index.html',
        viewModel.Context,
    )

def decision(request, cn):
    """Renders a single decision."""
    assert isinstance(request, HttpRequest)

    decision = DecisionBibliographyModel.objects.GetFromCaseNumber(cn)
    viewModel = DecisionVM.SingleDecisionViewModel(decision)
    return render(
        request,
        'app/decisionbibliography.html',
        viewModel.Context,
    )        

def search(request):
    """Searches the DB by case number."""
    
    if not request.method == 'POST':
        return redirect(request.META['HTTP_REFERER'])
        
    query = Formatters.formatCaseNumber(request.POST.get('q', None))
    return redirect (decision, query)

def boardtimelines(request):
    """Renders a view of board timelines."""
    assert isinstance(request, HttpRequest)

    viewModel = TimeLinesVM.TimeLinesViewModel()
    return render(
        request,
        'app/boardtimelines.html',
        viewModel.Context,
        )
        

def board(request, bd):
    """Renders a view of board information."""
    assert isinstance(request, HttpRequest)
    viewModel = BoardVM.BoardViewModel(bd)
    return render(
        request,
        'app/board.html',
        viewModel.Context,
        )



