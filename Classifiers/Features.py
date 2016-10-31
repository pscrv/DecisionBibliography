

class ClassificationFeatures(object):

    def __init__(self):
        self.__features = {}

    def MakeFeature(self, name):
        if not self.__features.get(name, []):
            self.__features[name] = []

    def AddFeature(self, name, value):
        feature = self.__features.get(name, [])
        feature.append(value)

    def GetFeature(self, name):
        return self.__features.get(name, [])

    def GetFeatures(self):
        return self.__features

    def RemoveFeature(self, name):
        if self.__features.get(name, None):
            features.pop(name)