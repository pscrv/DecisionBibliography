from Decisions.ViewModels.Base import VMBase
from Decisions.DBProxy import DecisionModelProxy


class  IndexViewModel(VMBase):

    def __init__(self):
        super(IndexViewModel, self).__init__()

        decisions = DecisionModelProxy.GetLatest(5)

        self.Context.update( {
            'decisions': decisions,
            'title': 'Welcome',
            } )
