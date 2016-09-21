"""
Definition of views.
"""

from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime

from . models import DecisionBibliographyModel
from . import Formatters

def home(request):

    #region experiement
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
   
    earliest = DecisionBibliographyModel.objects.order_by('DecisionDate')[0]
    latest = DecisionBibliographyModel.objects.order_by('-DecisionDate')[0]
    context =  {
            'title':'About',
            'year':datetime.now().year,
            'GCount': DecisionBibliographyModel.objects.filter(CaseNumber__startswith='G').count(),
            'RCount': DecisionBibliographyModel.objects.filter(CaseNumber__startswith='R').count(),
            'JCount': DecisionBibliographyModel.objects.filter(CaseNumber__startswith='J').count(),
            'TCount': DecisionBibliographyModel.objects.filter(CaseNumber__startswith='T').count(),
            'WCount': DecisionBibliographyModel.objects.filter(CaseNumber__startswith='W').count(),
            'DCount': DecisionBibliographyModel.objects.filter(CaseNumber__startswith='D').count(),
            'TotalCount': DecisionBibliographyModel.objects.count(),
            'Earliest': earliest,
            'EarliestDate': earliest.DecisionDate,
            'Latest': latest,
            'LatestDate': latest.DecisionDate,
            }

    return render(
        request,
        'app/index.html',
        context,
    )

def decision(request, cn):
    """Renders a single decision."""
    assert isinstance(request, HttpRequest)

    dec = DecisionBibliographyModel.objects.GetFromCaseNumber(cn)
    return __renderSingleDecision(request, dec)

def search(request):
    """Searches the DB by case number."""
    
    if not request.method == 'POST':
        return redirect(request.META['HTTP_REFERER'])
        
    query = Formatters.formatCaseNumber(request.POST.get('q', None))
    return redirect (decision, query)

def boardtimelines(request):
    """Renders a view of board timelines."""
    assert isinstance(request, HttpRequest)
    
    
    from . DBAnalyser import Analyser
    from . import DateHelpers
    
    analyser = Analyser()
    analyser.Analyse()
    timelines = analyser.GetAllBoardTimelines()

    yearline = timelines['years']
    timelines.pop('')
    timelines.pop('years')    

    context = {'years': yearline, 'boardtls': sorted(timelines.items())}
    return render(
        request,
        'app/boardtimelines.html',
        context,
    )


        


#region utility methods
def __renderSingleDecision(request, decision):
    context = __makeDecisionContext(decision)
    return render(
        request,
        'app/decisionbibliography.html',
        context,
    )        

def __makeDecisionContext(decision, msg = ''):
    message = msg
    if message == '' and not decision:
        message = 'Not found'
    context = {
        'title': 'DecisionView',
        'message': message,
        'year': datetime.now().year,
        'decision': decision,
        'citedDecisions': __getCitedDecisions(decision),
    }
    return context

def __getCitedDecisions(decision):
    citedDecisions = []
    if not decision:
        return citedDecisions
    if decision.CitedCases == "":
        return citedDecisions
    for case in decision.CitedCases.split(','):
        case = case.strip()
        dec = DecisionBibliographyModel.objects.GetFromCaseNumber(case)
        if dec:
            citedDecisions.append(dec)
    return citedDecisions
#endregion