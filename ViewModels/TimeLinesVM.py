from app.Analysers.Persistent import PersistentAnalyser


class TimeLinesViewModel(object):
        
    __analyser = PersistentAnalyser()

    def __init__(self):
        timelines = self.__analyser.GetAllBoardTimelines()

        yearline = timelines['years']
        timelines.pop('')
        timelines.pop('years')    

        self.Context = {'years': yearline, 'boardtls': sorted(timelines.items())}