from ViewModels.Base import VMBase
from Analysers.Persistent import PersistentAnalyser


class TimeLinesViewModel(VMBase):
        
    __analyser = PersistentAnalyser()

    def __init__(self):
        super(TimeLinesViewModel, self).__init__()

        timelines = self.__analyser.GetAllBoardTimelines()

        yearline = timelines['years']
        timelines.pop('')
        timelines.pop('years')    

        self.Context.update( {
            'years': yearline, 
            'boardtls': sorted(timelines.items())
            } )