from ViewModels.Base import VMBase
from app.DBProxy import DecisionModelProxy


class  IndexViewModel(VMBase):

    def __init__(self):
        super(IndexViewModel, self).__init__()

        decisions = DecisionModelProxy.GetLatestByDecisionDate(5)

        self.Context.update( {
            'decisions': decisions,
            'title': 'Welcome',
            } )