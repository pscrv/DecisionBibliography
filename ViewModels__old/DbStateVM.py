from ViewModels.Base import VMBase
from app.DBProxy import DecisionModelProxy



class DbStateViewModel(VMBase):
     
    def __init__(self):
        super(DbStateViewModel, self).__init__()
        
        earliest = DecisionModelProxy.GetEarliestByDecisionDate()[0]
        latest = DecisionModelProxy.GetLatestByDecisionDate()[0]
        self.Context.update ( {
            'title':'About',
            'GCount': DecisionModelProxy.GetCasetypeCount('G'),
            'RCount': DecisionModelProxy.GetCasetypeCount('R'),
            'JCount': DecisionModelProxy.GetCasetypeCount('J'),
            'TCount': DecisionModelProxy.GetCasetypeCount('T'),
            'WCount': DecisionModelProxy.GetCasetypeCount('W'),
            'DCount': DecisionModelProxy.GetCasetypeCount('D'),
            'TotalCount': DecisionModelProxy.GetBibliographyCount(),
            'TotalTxtCount': DecisionModelProxy.GetTextCount(),
            'Earliest': earliest,
            'EarliestDate': earliest.DecisionDate,
            'Latest': latest,
            'LatestDate': latest.DecisionDate,
            } )
