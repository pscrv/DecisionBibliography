from app.DBAnalyser import PublishedDecisionTimelineAnalyser


class TimeLinesViewModel(object):
        
    analyser = PublishedDecisionTimelineAnalyser()

    def __init__(self):       
        self.analyser.AnalysePublishedDecisionTimelines()
        timelines = self.analyser.GetAllBoardTimelines()

        yearline = timelines['years']
        timelines.pop('')
        timelines.pop('years')    

        self.Context = {'years': yearline, 'boardtls': sorted(timelines.items())}