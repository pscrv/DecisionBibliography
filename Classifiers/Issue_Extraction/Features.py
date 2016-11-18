import abc
from Helpers import TextHelpers

class ClassificationFeature(abc.ABC):

    @abc.abstractmethod
    def CountOccurrences(self, text : str):
        pass


class WordClassificationFeature(ClassificationFeature):

    def __init__(self, word : str):
        self._word = word

    def CountOccurrences(self, text):
        return TextHelpers.countwordoccurences(self._word, text)

    def __repr__(self):
        return '{}({})'.format(self.__class__, self._word)

    

class StringClassificationFeature(ClassificationFeature):

    def __init__(self, string : str):
        self._string = string

    def CountOccurrences(self, text):
        return TextHelpers.countstringoccurencesinword(self._string, text)

    def __repr__(self):
        return '{}({})'.format(self.__class__, self._string)


class StringInWordPairClassificationFeature(ClassificationFeature):

    def __init__(self, string1 : str, string2 : str):
        self._string1 = string1
        self._string2 = string2

    def CountOccurrences(self, text):
        return TextHelpers.countstringpairsinwords(self._string1, self._string2, 0, text)

    def __repr__(self):
        return '{}({} +++ {})'.format(self.__class__, self._string1, self._string2)




