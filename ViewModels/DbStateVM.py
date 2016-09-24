class DbStateViewModel(object):
     
    def __init__(self):
        from app.models import DecisionBibliographyModel as DB
        earliest = DB.objects.order_by('DecisionDate')[0]
        latest = DB.objects.order_by('-DecisionDate')[0]
        self.Context =  {
            'title':'About',
            'GCount': DB.objects.filter(CaseNumber__startswith='G').count(),
            'RCount': DB.objects.filter(CaseNumber__startswith='R').count(),
            'JCount': DB.objects.filter(CaseNumber__startswith='J').count(),
            'TCount': DB.objects.filter(CaseNumber__startswith='T').count(),
            'WCount': DB.objects.filter(CaseNumber__startswith='W').count(),
            'DCount': DB.objects.filter(CaseNumber__startswith='D').count(),
            'TotalCount': DB.objects.count(),
            'Earliest': earliest,
            'EarliestDate': earliest.DecisionDate,
            'Latest': latest,
            'LatestDate': latest.DecisionDate,
            }