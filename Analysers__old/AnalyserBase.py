from abc import ABC, abstractmethod
from datetime import datetime, timedelta

class CachingBase(ABC):

    @abstractmethod
    def _analyseAndCache(self, key):
        pass


    def __init__(self, cachetimelimit: timedelta = timedelta(days=1)):
        self._cache = {}
        self.__cacheTimeLimit = cachetimelimit

    
    def _cachedKeyList(self):
        self.__removeOldFromCache()
        return [key for key in self._cache]
    
    
    def GetAnalysis(self, key):
        if self.__needToAnalyse(key):
            analysis = self._analyseAndCache(key)
        else:
            analysis = self._cache[key]            
        return analysis

    
    def __needToAnalyse(self, key):
        self.__removeOldFromCache()
        return key not in self._cache

    
    def __removeOldFromCache(self):
        self._cache = { key: value 
                        for key, value 
                        in self._cache.items() 
                        if value.Age < self.__cacheTimeLimit }
