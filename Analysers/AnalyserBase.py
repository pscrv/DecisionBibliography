from abc import ABC, abstractmethod
from datetime import datetime, timedelta

class CachingBase(ABC):

    @abstractmethod
    def _analyseAndCache(key):
        pass


    def __init__(self, cachetimelimit:timedelta = timedelta(days=1)):
        self._cache = {}
        self._cacheTimeLimit = cachetimelimit

    
    def _cachedKeyList(self):
        return [key for key in self._cache]
    
    
    def GetAnalysis(self, key):
        needToAnalyse = self._needToAnalyse(key)
        if needToAnalyse:
            analysis = self._analyseAndCache(key)
        else:
            analysis = self._cache[key]            
        return analysis

    
    def _needToAnalyse(self, key):
        self._removeOldFromCache()
        return key not in self._cache

    
    def _removeOldFromCache(self):
        self._cache = { key: value 
                        for key, value 
                        in self._cache.items() 
                        if value.Age < self._cacheTimeLimit }