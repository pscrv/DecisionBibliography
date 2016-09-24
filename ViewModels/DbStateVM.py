class DbStateViewModel(object):
     
    def __init__(self):
        from app.models import DecisionBibliographyModel as bibDB, DecisionTextModel as txtDB
        
        earliest = bibDB.objects.order_by('DecisionDate')[0]
        latest = bibDB.objects.order_by('-DecisionDate')[0]
        self.Context =  {
            'title':'About',
            'GCount': bibDB.objects.filter(CaseNumber__startswith='G').count(),
            'RCount': bibDB.objects.filter(CaseNumber__startswith='R').count(),
            'JCount': bibDB.objects.filter(CaseNumber__startswith='J').count(),
            'TCount': bibDB.objects.filter(CaseNumber__startswith='T').count(),
            'WCount': bibDB.objects.filter(CaseNumber__startswith='W').count(),
            'DCount': bibDB.objects.filter(CaseNumber__startswith='D').count(),
            'TotalCount': bibDB.objects.count(),
            'TotalTxtCount': txtDB.objects.count(),
            'Earliest': earliest,
            'EarliestDate': earliest.DecisionDate,
            'Latest': latest,
            'LatestDate': latest.DecisionDate,
            }