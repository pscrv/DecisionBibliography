import abc
from Helpers import TextHelpers
from Serialisation.Simple import serialisable


class ClassificationFeature(abc.ABC):

    @abc.abstractproperty
    def Name(self):
        pass

    @abc.abstractmethod
    def CountOccurrences(self, text : str):
        pass

    
@serialisable
class WordClassificationFeature(ClassificationFeature):

    def __init__(self, word : str):
        self._word = word

    @property
    def Name(self):
        return self._word

    def CountOccurrences(self, text):
        return TextHelpers.countwordoccurences(self._word, text)
   
    def __repr__(self):
        return 'WordClassificationFeature({})'.format(self._word)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self._word == other._word

    def __hash__(self):
        return self._word.__hash__()

    
    
@serialisable
class StringClassificationFeature(ClassificationFeature):

    def __init__(self, string : str):
        self._string = string

    @property
    def Name(self):
        return self._string

    def CountOccurrences(self, text):
        return TextHelpers.countstringoccurencesinword(self._string, text)

    def __repr__(self):
        return 'StringClassificationFeature({})'.format(self._string)

    
@serialisable
class StringInWordPairClassificationFeature(ClassificationFeature):

    def __init__(self, string1 : str, string2 : str):
        self._string1 = string1
        self._string2 = string2

    @property
    def Name(self):
        return self._string1 + '#' + self._string2

    def CountOccurrences(self, text):
        return TextHelpers.countstringpairsinwords(self._string1, self._string2, 0, text)

    def __repr__(self):
        return 'StringInWordPairClassificationFeature({} +++ {})'.format(self._string1, self._string2)






 
class Tryout(ClassificationFeature):

    def __init__(self, word : str):
        self._word = word

    @property
    def Name(self):
        return self._word

    def CountOccurrences(self, text):
        return TextHelpers.countwordoccurences(self._word, text)

    def __repr__(self):
        return 'WordClassificationFeature({})'.format(self._word)




