from . models import DecisionBibliographyModel
from . import DateHelpers

def _getMonthlyOutputTLs():

    decisions = DecisionBibliographyModel.objects
    start = DateHelpers.FirstOfThisMonth(decisions.order_by('DecisionDate').first().DecisionDate)
    end = DateHelpers.EndOfThisMonth(decisions.order_by('-DecisionDate').first().DecisionDate)

    output = {}
    for dt in DateHelpers.MonthIterator(start, end):
        output[dt] = decisions.filter(DecisionDate = dt).count()

    x = True
    y = False

