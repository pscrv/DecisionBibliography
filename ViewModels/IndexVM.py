from app.models import DecisionBibliographyModel as DB

class  IndexViewModel(object):

    def __init__(self):

        decisions = DB.objects.order_by('-DecisionDate')[:5]

        self.Context = {
            'decisions': decisions,
            'title': 'Welcome',
            }