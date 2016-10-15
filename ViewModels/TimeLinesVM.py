from app.DBAnalyser import PublishedDecisionTimelineAnalyser, PersistentAnalyser


class TimeLinesViewModel(object):
        
    #__analyser = PublishedDecisionTimelineAnalyser()
    __analyser = PersistentAnalyser()

    def __init__(self):       
        #self.__analyser.AnalysePublishedDecisionTimelines()
        timelines = self.__analyser.GetAllBoardTimelines()

        yearline = timelines['years']
        timelines.pop('')
        timelines.pop('years')    

        self.Context = {'years': yearline, 'boardtls': sorted(timelines.items())}