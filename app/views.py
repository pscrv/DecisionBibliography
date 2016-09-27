"""
Definition of views.
"""

from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.template import RequestContext

from . models import DecisionBibliographyModel, DecisionTextModel
from ViewModels import BoardVM
from ViewModels import DbStateVM
from ViewModels import DecisionVM 
from ViewModels import TimeLinesVM 
from ViewModels import BoardVM 
from ViewModels import IndexVM
from app import Formatters, DBPopulator


def home(request):

    #region experiement
    #from . models import DecisionTextModel
    #from . DBPopulator import TextGetter
    #dec = DecisionBibliographyModel.objects.GetFromCaseNumber('J 0001/78')
    #textGetter = TextGetter()
    #txt = textGetter.Get_Text(dec)
    #x = 1
    #endregion

    # region comment out this, if db is not being populated
    #start = datetime(1990, 1, 1)
    #end = datetime(1999, 12, 31)

    #from . DBPopulator import BibliographyGetter
    #bg = BibliographyGetter()
    #bg.Get_FromDate_ToDate(start, end) 
    # endregion

    """Renders the home page."""
    assert isinstance(request, HttpRequest)

    viewModel = IndexVM.IndexViewModel()
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
        'app/decision.html',
        viewModel.Context,
    )        

def search(request):
    """Searches the DB by case number."""
    from app import Formatters
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

def about(request):

    #region experiement
    #from . models import DecisionTextModel
    #from . DBPopulator import TextGetter
    #dec = DecisionBibliographyModel.objects.GetFromCaseNumber('J 0001/78')
    #textGetter = TextGetter()
    #txt = textGetter.Get_Text(dec)
    #x = 1
    #endregion

    # region comment out this, if db is not being populated
    #start = datetime(1990, 1, 1)
    #end = datetime(1999, 12, 31)

    #from . DBPopulator import BibliographyGetter
    #bg = BibliographyGetter()
    #bg.Get_FromDate_ToDate(start, end) 
    # endregion

    """Renders the home page."""
    assert isinstance(request, HttpRequest)

    viewModel = DbStateVM.DbStateViewModel()
    return render(
        request,
        'app/about.html',
        viewModel.Context,
    )



