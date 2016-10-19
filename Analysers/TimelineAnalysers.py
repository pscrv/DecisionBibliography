

class TimelineAnalyser(object):

    def __init__(self, cachetimelimit:timedelta = timedelta(days=1)):
        self.__cache = {}
        self.__cacheTimeLimit = cachetimelimit

        
    def GetTimelines(self):
        self.__removeOldFromCache()
        needToAnalyse = self.__needToAnalyse()
        if needToAnalyse:
            analysis = self.__analyseAndCacheBoard()
        else:
            analysis = self.__cache[self.__workingBoard]            
        return analysis

    

    def __removeOldFromCache(self):
        self.__cache = { board: timeline 
                        for board, timeline 
                        in self.__cache.items() 
                        if timeline.Age < self.__cacheTimeLimit }