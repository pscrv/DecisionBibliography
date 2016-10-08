from app.DBProxy import DecisionModelProxy

class  IndexViewModel(object):

    def __init__(self):

        #decisions = DB.objects.FilterOnlyPrLanguage().order_by('-DecisionDate')[:5]
        decisions = DecisionModelProxy.GetLatestByDecisionDate(5)

        self.Context = {
            'decisions': decisions,
            'title': 'Welcome',
            }